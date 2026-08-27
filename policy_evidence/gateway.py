from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from .adapter import _create_for_gateway


READ_TOOLS = {
    "policy.definitions.list": "list_definitions",
    "policy.initiatives.list": "list_initiatives",
    "policy.compliance.list": "list_compliance_states",
    "policy.remediations.list": "list_remediations",
}
DENIED_WRITE_TOOLS = {"policy.remediation.invoke", "policy.assignment.create", "policy.exemption.create"}
IDENTITY_CONTRACT = {
    "synthetic-agent-compliance-reader": {
        "granted_scopes": ("synthetic-scope-platform",),
        "denied_scopes": ("synthetic-scope-restricted",),
    }
}


@dataclass(frozen=True)
class GatewayResult:
    status: int
    decision: str
    reason: str
    data: list[dict[str, Any]]
    reached_adapter: bool


class Gateway:
    def __init__(self, fixtures: dict[str, Any]) -> None:
        self._fixtures = fixtures
        self._adapter = _create_for_gateway(fixtures)
        self.adapter_calls: list[str] = []

    def dispatch(self, call: dict[str, str], identity_id: str) -> GatewayResult:
        identity = self._identity(identity_id)
        scope = call.get("scope_id", "")
        tool = call.get("tool", "")
        if scope not in identity["granted_scopes"] or scope in identity["denied_scopes"]:
            return GatewayResult(403, "deny", "identity lacks the exact requested scope", [], False)
        if tool in DENIED_WRITE_TOOLS:
            return GatewayResult(403, "deny", "write tools are unavailable in this read-only workflow", [], False)
        method_name = READ_TOOLS.get(tool)
        if method_name is None:
            return GatewayResult(403, "deny", "tool is not in the static allowlist", [], False)
        self.adapter_calls.append(tool)
        data = getattr(self._adapter, method_name)(scope)
        return GatewayResult(200, "allow", "identity, scope and tool are allowed", data, True)

    def _identity(self, identity_id: str) -> dict[str, Any]:
        matches = [item for item in self._fixtures["identities"] if item["id"] == identity_id]
        if len(matches) != 1:
            raise PermissionError("identity must resolve exactly once")
        identity = matches[0]
        expected = IDENTITY_CONTRACT.get(identity_id)
        if expected is None:
            raise PermissionError("identity is not in the static identity contract")
        if tuple(identity["granted_scopes"]) != expected["granted_scopes"]:
            raise PermissionError("granted scopes differ from the static identity contract")
        if tuple(identity["denied_scopes"]) != expected["denied_scopes"]:
            raise PermissionError("denied scopes differ from the static identity contract")
        return identity
