from __future__ import annotations

from typing import Any


class _GatewayCapability:
    pass


_CAPABILITY = _GatewayCapability()


class PolicyFixtureAdapter:
    """Read-only fixture access. Only the gateway owns the construction capability."""

    def __init__(self, capability: object, fixtures: dict[str, Any]) -> None:
        if capability is not _CAPABILITY:
            raise PermissionError("adapter construction is restricted to the gateway")
        self._fixtures = fixtures

    def list_definitions(self, scope_id: str) -> list[dict[str, Any]]:
        return list(self._fixtures["definitions"])

    def list_initiatives(self, scope_id: str) -> list[dict[str, Any]]:
        return list(self._fixtures["initiatives"])

    def list_compliance_states(self, scope_id: str) -> list[dict[str, Any]]:
        return [item for item in self._fixtures["compliance_states"] if item["scope_id"] == scope_id]

    def list_remediations(self, scope_id: str) -> list[dict[str, Any]]:
        return [item for item in self._fixtures["remediations"] if item["scope_id"] == scope_id]


def _create_for_gateway(fixtures: dict[str, Any]) -> PolicyFixtureAdapter:
    return PolicyFixtureAdapter(_CAPABILITY, fixtures)

