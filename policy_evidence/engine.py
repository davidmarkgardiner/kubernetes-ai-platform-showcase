from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from .gateway import Gateway
from .validation import canonical_bytes, load_and_validate


def run(fixtures_path: Path, plan_path: Path) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    fixtures, fixture_sha256 = load_and_validate(fixtures_path)
    plan = json.loads(plan_path.read_text())
    _validate_plan(plan)
    gateway = Gateway(fixtures)
    trace_id = "synthetic-trace-001"
    spans: list[dict[str, Any]] = []
    evidence: list[dict[str, Any]] = []
    denials: list[dict[str, Any]] = []

    for index, call in enumerate(plan["calls"], start=1):
        result = gateway.dispatch(call, plan["identity_id"])
        span = {
            "id": f"synthetic-span-{index:03d}",
            "trace_id": trace_id,
            "component": "adapter" if result.reached_adapter else "gateway",
            "tool": call["tool"],
            "status": result.status,
            "reached_adapter": result.reached_adapter,
        }
        spans.append(span)
        if result.status == 403:
            denials.append({"tool": call["tool"], "status": 403, "reason": result.reason, "span_id": span["id"]})
        for item in result.data:
            if call["tool"] != "policy.compliance.list":
                continue
            evidence.append({
                "id": f"synthetic-evidence-{len(evidence) + 1:03d}",
                "source_object_id": item["id"],
                "assertion": f"{item['resource_id']} is {item['state']} for {item['definition_id']}",
                "outcome": item["state"],
                "identity_id": plan["identity_id"],
                "scope_id": item["scope_id"],
                "control_id": item["id"],
                "trace_id": trace_id,
                "span_id": span["id"],
                "fixture_sha256": fixture_sha256,
                "confidence": "synthetic_deterministic",
            })

    bundle = {
        "run_id": fixtures["manifest"]["run_id"],
        "fixture_set_version": fixtures["manifest"]["fixture_set_version"],
        "fixture_sha256": fixture_sha256,
        "synthetic": True,
        "identity_id": plan["identity_id"],
        "evidence": evidence,
        "denials": denials,
        "summary": {
            "read_calls": len(gateway.adapter_calls),
            "denials": len(denials),
            "plan_deviations": 0,
            "successful_writes": 0,
        },
    }
    return bundle, spans


def compare_before_dispatch(requested_call: dict[str, str], plan: dict[str, Any]) -> dict[str, Any] | None:
    if requested_call not in plan["calls"]:
        return {
            "type": "plan_deviation",
            "tool": requested_call.get("tool", ""),
            "gateway_calls": 0,
            "adapter_calls": 0,
        }
    return None


def write_outputs(bundle: dict[str, Any], spans: list[dict[str, Any]], output_dir: Path) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    (output_dir / "bundle.json").write_bytes(canonical_bytes(bundle))
    trace = b"".join(canonical_bytes(span) for span in spans)
    (output_dir / "trace.jsonl").write_bytes(trace)


def _validate_plan(plan: dict[str, Any]) -> None:
    if set(plan) != {"plan_id", "identity_id", "calls"}:
        raise ValueError("plan uses a closed schema")
    if not str(plan["plan_id"]).startswith("synthetic-plan-"):
        raise ValueError("plan id must be synthetic")
    for call in plan["calls"]:
        if set(call) != {"tool", "scope_id"}:
            raise ValueError("call uses a closed schema")

