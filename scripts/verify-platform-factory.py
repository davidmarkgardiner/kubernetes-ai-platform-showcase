#!/usr/bin/env python3
"""Fail-closed structural verification for the sanitized platform-factory slice."""

from __future__ import annotations

import json
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FACTORY = ROOT / "platform-factory"
RECEIPT = ROOT / "evidence" / "platform-factory-receipt.json"


def require(path: str, markers: list[str]) -> None:
    text = (FACTORY / path).read_text(encoding="utf-8")
    missing = [marker for marker in markers if marker not in text]
    if missing:
        raise SystemExit(f"{path}: missing required markers: {missing}")


required_files = [
    "README.md",
    "definitions/team-environment.yaml",
    "definitions/aks-cluster-blueprint.yaml",
    "examples/team-environment.yaml",
    "gitops/source.yaml",
    "gitops/platform-kustomization.yaml",
    "gitops/applications-kustomization.yaml",
    "gitops/helmrelease.yaml",
    "addons/external-secrets.yaml",
    "addons/kyverno-policy.yaml",
    "rbac/kro-team-environment-role.yaml",
]
for relative in required_files:
    if not (FACTORY / relative).is_file():
        raise SystemExit(f"missing required file: platform-factory/{relative}")

require(
    "definitions/team-environment.yaml",
    [
        "apiVersion: kro.run/v1alpha1",
        "kind: ResourceGraphDefinition",
        "kind: TeamEnvironment",
        "kind: Namespace",
        "kind: ResourceQuota",
        "kind: LimitRange",
        "kind: ServiceAccount",
        "kind: NetworkPolicy",
        "name: default-deny",
    ],
)
require(
    "definitions/aks-cluster-blueprint.yaml",
    [
        "kind: AzureKubernetesCluster",
        "resources.azure.com/v1api20200601",
        "kind: ResourceGroup",
        "containerservice.azure.com/v1api20240901",
        "kind: ManagedCluster",
        "workloadIdentity:",
        "definition-only-not-applied",
    ],
)
require("gitops/source.yaml", ["source.toolkit.fluxcd.io/v1", "github.com/example/platform-fleet.git"])
require("gitops/platform-kustomization.yaml", ["kustomize.toolkit.fluxcd.io/v1", "prune: true", "wait: true"])
require("gitops/applications-kustomization.yaml", ["dependsOn:", "name: platform-controllers", "prune: true", "wait: true"])
require("gitops/helmrelease.yaml", ["helm.toolkit.fluxcd.io/v2", "kind: HelmRelease", "version: \""])
require("addons/external-secrets.yaml", ["external-secrets.io/v1", "kind: ClusterSecretStore", "kind: ExternalSecret", "fake:", "synthetic-demo-value"])
require("addons/kyverno-policy.yaml", ["kyverno.io/v1", "kind: ClusterPolicy", "validationFailureAction: Enforce", "platform.example.com/owner"])
require("rbac/kro-team-environment-role.yaml", ["rbac.kro.run/aggregate-to-controller: \"true\"", "teamenvironments/status"])

all_text = "\n".join(path.read_text(encoding="utf-8") for path in FACTORY.rglob("*") if path.is_file())

forbidden_patterns = {
    "Azure blueprint instance": r"(?m)^kind:\s*AzureKubernetesCluster\s*$",
    "UUID-shaped cloud identifier": r"\b[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}\b",
    "private key": r"BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY",
    "GitHub token": r"ghp_[A-Za-z0-9]{20,}",
    "OpenAI-shaped key": r"sk-[A-Za-z0-9]{20,}",
}
for label, pattern in forbidden_patterns.items():
    if re.search(pattern, all_text):
        raise SystemExit(f"forbidden {label} detected")

if "provider:\n    azurekv:" in all_text or "provider:\n    aws:" in all_text or "provider:\n    gcpsm:" in all_text:
    raise SystemExit("real external-secret provider detected; only the fake provider is allowed")

receipt = {
    "schemaVersion": "1.0",
    "scope": "sanitized-platform-factory",
    "result": "PASS",
    "checks": [
        {"capability": "KRO TeamEnvironment composition", "status": "STRUCTURALLY_VERIFIED", "runtime": "run scripts/platform-factory-kind-smoke.sh for local proof"},
        {"capability": "KRO plus Azure Service Operator cluster blueprint", "status": "STRUCTURALLY_VERIFIED", "runtime": "NOT_PROVEN; definition is never applied"},
        {"capability": "Flux pull-based reconciliation", "status": "STRUCTURALLY_VERIFIED", "runtime": "NOT_PROVEN; example source is inert"},
        {"capability": "External Secrets integration", "status": "STRUCTURALLY_VERIFIED", "runtime": "NOT_PROVEN; fake provider only"},
        {"capability": "Kyverno ownership guardrail", "status": "STRUCTURALLY_VERIFIED", "runtime": "NOT_PROVEN in this receipt"},
        {"capability": "No Azure cluster instance or cloud identifiers", "status": "VERIFIED", "runtime": "not applicable"},
    ],
}
RECEIPT.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")
print("PLATFORM_FACTORY_VERIFY_OK")
