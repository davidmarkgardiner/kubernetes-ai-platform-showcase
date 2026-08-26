# Proof register

This register prevents architecture and ambition from being presented as runtime proof.

| Capability | Status in this repository | Evidence |
|---|---|---|
| Least-privilege domain/action policy | Implemented and tested | `internal/policy`, `go test ./...` |
| Human review before consequential action | Implemented as a decision contract | policy tests; execution is deliberately external |
| Confidential compliance export denial | Implemented and tested | `TestConfidentialExportDenied` |
| Cross-domain evidence validation | Implemented and tested | `tools/evidence_router.py`, Python tests |
| Secret-like input rejection | Implemented and tested | `test_rejects_secret_like_content` |
| Platform, SRE, compliance and data examples | Synthetic demonstration | `examples/`, `docs/case-studies.md` |
| Kubernetes networking/storage/security integration | Architecture and career capability | backend-specific runtime proof remains outside this repository |
| kagent and agentgateway integration | Implemented and runtime-tested on disposable Kind | `scripts/kind-demo-*.sh`, `deploy/kind/`, `evidence/runtime/kind-showcase-receipt.json` |
| Prompt-policy denial | Implemented and runtime-tested on disposable Kind | smoke test observes HTTP 403 from the configured AgentgatewayPolicy |
| Trace and token telemetry | Implemented and runtime-tested on disposable Kind | correlated synthetic trace ID and Agentgateway token metric in the runtime receipt |
| Live-model answer quality | Not claimed | the reproducible runtime intentionally uses a keyless deterministic mock backend |
| Autonomous production remediation | Not claimed | prohibited by repository boundary |
| Employer production deployment | Not claimed | no employer material is present |

## Promotion rule

A row may move from architecture or synthetic demonstration to implemented/live only when the repository contains a reproducible command, exact version/context, sanitized receipt, limitations and last-verified date.
