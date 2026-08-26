#!/usr/bin/env python3
"""Validate and group synthetic evidence for governed AI workflow demonstrations."""

from __future__ import annotations

import json
import re
import sys
from collections import defaultdict
from pathlib import Path

ALLOWED_DOMAINS = {"platform", "sre", "compliance", "data"}
SECRET_PATTERN = re.compile(r"(?i)(password|secret|token|api[_-]?key)\s*[:=]\s*\S+")


def route(items: list[dict]) -> dict:
    grouped: dict[str, list[dict]] = defaultdict(list)
    rejected: list[dict] = []

    for index, item in enumerate(items):
        domain = str(item.get("domain", "")).strip().lower()
        claim = str(item.get("claim", "")).strip()
        citation = str(item.get("citation", "")).strip()
        confidence = str(item.get("confidence", "")).strip().lower()

        errors = []
        if domain not in ALLOWED_DOMAINS:
            errors.append("domain is not allow-listed")
        if not claim:
            errors.append("claim is required")
        if not citation:
            errors.append("citation is required")
        if confidence not in {"high", "medium", "low"}:
            errors.append("confidence must be high, medium or low")
        if SECRET_PATTERN.search(json.dumps(item)):
            errors.append("possible secret-bearing content")

        if errors:
            rejected.append({"index": index, "errors": errors})
            continue

        status = {"high": "supported", "medium": "partial", "low": "needs-review"}[confidence]
        grouped[domain].append({**item, "status": status})

    return {
        "schema": "showcase.evidence-bundle/v1",
        "domains": dict(sorted(grouped.items())),
        "rejected": rejected,
        "summary": {
            "accepted": sum(len(values) for values in grouped.values()),
            "rejected": len(rejected),
            "human_review_required": any(
                finding["status"] != "supported"
                for findings in grouped.values()
                for finding in findings
            ),
        },
    }


def main() -> int:
    if len(sys.argv) != 2:
        print("usage: evidence_router.py findings.json", file=sys.stderr)
        return 2
    source = Path(sys.argv[1])
    try:
        data = json.loads(source.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        print(f"invalid evidence input: {exc}", file=sys.stderr)
        return 1
    if not isinstance(data, list):
        print("invalid evidence input: expected a JSON array", file=sys.stderr)
        return 1
    print(json.dumps(route(data), indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
