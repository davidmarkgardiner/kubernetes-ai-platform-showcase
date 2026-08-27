from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


ROOT_FIELDS = {"manifest", "identities", "definitions", "initiatives", "compliance_states", "remediations"}
FIELDS = {
    "manifest": {"fixture_set_version", "synthetic", "run_id"},
    "identities": {"id", "granted_scopes", "denied_scopes"},
    "definitions": {"id", "display_name", "effect"},
    "initiatives": {"id", "definition_ids"},
    "compliance_states": {"id", "definition_id", "initiative_id", "scope_id", "resource_id", "state"},
    "remediations": {"id", "definition_id", "scope_id", "status"},
}
PREFIXES = (
    "synthetic-def-", "synthetic-init-", "synthetic-scope-", "synthetic-resource-",
    "synthetic-remediation-", "synthetic-agent-", "synthetic-control-", "synthetic-run-",
)


def canonical_bytes(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":")) + "\n").encode()


def load_and_validate(path: Path) -> tuple[dict[str, Any], str]:
    raw = path.read_bytes()
    data = json.loads(raw)
    _expect_fields(data, ROOT_FIELDS, "root")
    if data["manifest"]["synthetic"] is not True:
        raise ValueError("manifest.synthetic must be true")
    _expect_fields(data["manifest"], FIELDS["manifest"], "manifest")

    for collection in ("identities", "definitions", "initiatives", "compliance_states", "remediations"):
        if not isinstance(data[collection], list):
            raise ValueError(f"{collection} must be a list")
        for index, item in enumerate(data[collection]):
            _expect_fields(item, FIELDS[collection], f"{collection}[{index}]")

    ids: list[str] = [data["manifest"]["run_id"]]
    for collection in ("identities", "definitions", "initiatives", "compliance_states", "remediations"):
        ids.extend(item["id"] for item in data[collection])
    scope_ids = {
        scope
        for identity in data["identities"]
        for scope in identity["granted_scopes"] + identity["denied_scopes"]
    }
    resource_ids = {item["resource_id"] for item in data["compliance_states"]}
    ids.extend(sorted(scope_ids | resource_ids))
    if len(ids) != len(set(ids)):
        raise ValueError("all fixture identifiers must be unique")
    for identifier in ids:
        if not isinstance(identifier, str) or not identifier.startswith(PREFIXES):
            raise ValueError(f"identifier is outside the synthetic namespaces: {identifier!r}")

    definitions = {item["id"] for item in data["definitions"]}
    initiatives = {item["id"] for item in data["initiatives"]}
    for item in data["initiatives"]:
        _require_refs(item["definition_ids"], definitions, f"initiative {item['id']}")
    for item in data["compliance_states"]:
        _require_refs([item["definition_id"]], definitions, f"compliance state {item['id']}")
        _require_refs([item["initiative_id"]], initiatives, f"compliance state {item['id']}")
        _require_refs([item["scope_id"]], scope_ids, f"compliance state {item['id']}")
        _require_refs([item["resource_id"]], resource_ids, f"compliance state {item['id']}")
    for item in data["remediations"]:
        _require_refs([item["definition_id"]], definitions, f"remediation {item['id']}")
        _require_refs([item["scope_id"]], scope_ids, f"remediation {item['id']}")

    return data, hashlib.sha256(raw).hexdigest()


def _expect_fields(value: dict[str, Any], allowed: set[str], label: str) -> None:
    if not isinstance(value, dict) or set(value) != allowed:
        raise ValueError(f"{label} fields must be exactly {sorted(allowed)}")


def _require_refs(references: list[str], targets: set[str], label: str) -> None:
    missing = [reference for reference in references if reference not in targets]
    if missing:
        raise ValueError(f"{label} has unresolved references: {missing}")

