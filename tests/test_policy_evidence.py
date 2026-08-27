from __future__ import annotations

import copy
import json
import tempfile
import unittest
from pathlib import Path

from policy_evidence.adapter import PolicyFixtureAdapter
from policy_evidence.engine import compare_before_dispatch, run
from policy_evidence.gateway import Gateway
from policy_evidence.validation import canonical_bytes, load_and_validate


ROOT = Path(__file__).parents[1]
FIXTURES = ROOT / "policy_evidence/fixtures/policy-set.json"
PLAN = ROOT / "policy_evidence/fixtures/plan.json"


class PolicyEvidenceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.fixtures, _ = load_and_validate(FIXTURES)
        self.plan = json.loads(PLAN.read_text())

    def test_repeatable_bundle_and_read_only_denial(self) -> None:
        first = run(FIXTURES, PLAN)
        second = run(FIXTURES, PLAN)
        self.assertEqual(canonical_bytes(first), canonical_bytes(second))
        bundle, spans = first
        self.assertEqual(bundle["summary"], {"read_calls": 5, "denials": 1, "plan_deviations": 0, "successful_writes": 0})
        denied = [span for span in spans if span["status"] == 403]
        self.assertEqual(len(denied), 1)
        self.assertFalse(denied[0]["reached_adapter"])
        self.assertEqual(denied[0]["component"], "gateway")

    def test_direct_adapter_access_fails(self) -> None:
        with self.assertRaises(PermissionError):
            PolicyFixtureAdapter(object(), self.fixtures)

    def test_unlisted_and_scope_escalation_fail_before_adapter(self) -> None:
        gateway = Gateway(self.fixtures)
        unknown = gateway.dispatch({"tool": "policy.unknown.list", "scope_id": "synthetic-scope-platform"}, "synthetic-agent-compliance-reader")
        escalated = gateway.dispatch({"tool": "policy.compliance.list", "scope_id": "synthetic-scope-restricted"}, "synthetic-agent-compliance-reader")
        self.assertEqual((unknown.status, escalated.status), (403, 403))
        self.assertEqual(gateway.adapter_calls, [])

    def test_identity_failures(self) -> None:
        call = {"tool": "policy.compliance.list", "scope_id": "synthetic-scope-platform"}
        for identity in ("", "synthetic-agent-unknown", "synthetic-agent-forged"):
            with self.assertRaises(PermissionError):
                Gateway(self.fixtures).dispatch(call, identity)
        duplicated = copy.deepcopy(self.fixtures)
        duplicated["identities"].append(copy.deepcopy(duplicated["identities"][0]))
        with self.assertRaises(PermissionError):
            Gateway(duplicated).dispatch(call, "synthetic-agent-compliance-reader")

    def test_identity_scope_tampering_is_denied(self) -> None:
        variants = []
        granted = copy.deepcopy(self.fixtures)
        granted["identities"][0]["granted_scopes"] = ["synthetic-scope-platform", "synthetic-scope-restricted"]
        variants.append(granted)
        denied = copy.deepcopy(self.fixtures)
        denied["identities"][0]["denied_scopes"] = []
        variants.append(denied)
        call = {"tool": "policy.compliance.list", "scope_id": "synthetic-scope-platform"}
        for fixtures in variants:
            with self.assertRaises(PermissionError):
                Gateway(fixtures).dispatch(call, "synthetic-agent-compliance-reader")

    def test_plan_deviation_stops_before_gateway(self) -> None:
        deviation = compare_before_dispatch(
            {"tool": "policy.assignment.create", "scope_id": "synthetic-scope-platform"}, self.plan
        )
        self.assertEqual(deviation["type"], "plan_deviation")
        self.assertEqual((deviation["gateway_calls"], deviation["adapter_calls"]), (0, 0))

    def test_unknown_fields_and_orphan_references_abort(self) -> None:
        for mutation in ("unknown", "orphan"):
            data = copy.deepcopy(self.fixtures)
            if mutation == "unknown":
                data["manifest"]["extra"] = "not-allowed"
            else:
                data["initiatives"][0]["definition_ids"].append("synthetic-def-missing")
            with tempfile.TemporaryDirectory() as directory:
                path = Path(directory) / "fixtures.json"
                path.write_text(json.dumps(data))
                with self.assertRaises(ValueError):
                    load_and_validate(path)

    def test_fixture_cannot_modify_allowlist(self) -> None:
        data = copy.deepcopy(self.fixtures)
        data["manifest"]["tool_allowlist"] = ["policy.assignment.create"]
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "fixtures.json"
            path.write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                load_and_validate(path)

    def test_engine_has_no_direct_adapter_import(self) -> None:
        source = (ROOT / "policy_evidence/engine.py").read_text()
        self.assertNotIn("policy_evidence.adapter", source)
        self.assertNotIn("from .adapter", source)

    def test_adapter_exports_no_write_method(self) -> None:
        exported = {name for name in dir(PolicyFixtureAdapter) if not name.startswith("_")}
        self.assertEqual(
            exported,
            {"list_definitions", "list_initiatives", "list_compliance_states", "list_remediations"},
        )

    def test_evidence_identity_matches_calling_identity(self) -> None:
        bundle, _ = run(FIXTURES, PLAN)
        self.assertTrue(bundle["evidence"])
        self.assertEqual(
            {item["identity_id"] for item in bundle["evidence"]},
            {bundle["identity_id"]},
        )


if __name__ == "__main__":
    unittest.main()
