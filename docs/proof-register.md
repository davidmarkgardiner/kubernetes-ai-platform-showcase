# Proof register

This register prevents architecture and ambition from being presented as runtime proof.

| Capability | Status in this repository | Evidence |
|---|---|---|
| Least-privilege domain/action policy | Implemented and tested | `internal/policy`, `go test ./...` |
| Human review before consequential action | Implemented as a decision contract | policy tests; execution is deliberately external |
| Confidential compliance export denial | Implemented and tested | `TestConfidentialExportDenied` |
| Public-safe Azure Policy-shaped evidence workflow | Implemented and deterministically tested | `policy_evidence/`, `tests/test_policy_evidence.py`, `evidence/policy-evidence-receipt.json` |
| Pre-dispatch plan deviation and write denial | Implemented and deterministically tested | deviation creates zero downstream calls; planned write is denied before adapter invocation |
| Fixture identity, scope and reference integrity | Implemented and deterministically tested | closed schemas, code-owned identity contract, orphan/tamper negative tests |
| Host-enforced no-network execution for policy workflow | Not proven | ordinary offline execution passed; an enforced isolation receipt is still required |
| Cross-domain evidence validation | Implemented and tested | `tools/evidence_router.py`, Python tests |
| Secret-like input rejection | Implemented and tested | `test_rejects_secret_like_content` |
| Platform, SRE, compliance and data examples | Public-safe reference scenarios | `examples/`, `docs/case-studies.md` |
| Kubernetes networking/storage/security integration | Architecture and career capability | backend-specific runtime proof remains outside this repository |
| kagent and agentgateway integration | Implemented and runtime-tested in an isolated Kubernetes reference | `scripts/kind-demo-*.sh`, `deploy/kind/`, `evidence/runtime/kind-showcase-receipt.json` |
| Prompt-policy denial | Implemented and runtime-tested in the isolated reference | smoke test confirms the restricted route is blocked before execution |
| Trace and token telemetry | Implemented and runtime-tested in the isolated reference | correlated safe-fixture trace ID and Agentgateway token metric in the runtime receipt |
| KRO self-service team environment | Implemented and runtime-tested in an isolated Kubernetes reference | `platform-factory/definitions/team-environment.yaml`, `scripts/platform-factory-kind-smoke.sh`, `evidence/runtime/platform-factory-kind-receipt.json` |
| Namespace, quota, limits, service account and default-deny composition | Implemented and runtime-tested in the isolated reference | public receipt records all five observed resources after reconciliation |
| KRO plus ASO Azure cluster blueprint | Definition-only; structurally verified, not applied | `platform-factory/definitions/aks-cluster-blueprint.yaml`; no custom-resource instance exists |
| Flux pull-based platform and application ordering | Structurally verified example; reconciliation not proven | v1 GitRepository/Kustomizations, v2 HelmRelease, prune/wait and `dependsOn` in `platform-factory/gitops/` |
| External Secrets contract | Structurally verified public-safe example; controller runtime not proven | v1 ClusterSecretStore and ExternalSecret using only the fake provider |
| Kyverno team ownership guardrail | Structurally verified example; admission runtime not proven | `platform-factory/addons/kyverno-policy.yaml` |
| Cloud provisioning from this showcase | Prohibited and absent | no `AzureKubernetesCluster` instance, credential, tenant or subscription identifier is stored |
| Live-model answer quality | Not claimed | the reproducible runtime intentionally uses a keyless deterministic mock backend |
| Autonomous production remediation | Not claimed | prohibited by repository boundary |
| Employer production deployment | Not claimed | no employer material is present |

## Promotion rule

A row may move from architecture or reference scenario to implemented/live only when the repository contains a reproducible command, exact version/context, sanitized receipt, limitations and last-verified date.
