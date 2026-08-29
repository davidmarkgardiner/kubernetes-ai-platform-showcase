# Capability map

## Kubernetes platform engineering

The positioning is Kubernetes-first rather than cloud-first. AKS is one substantial delivery environment, alongside experience with self-managed and other managed Kubernetes platforms.

| Platform concern | Demonstration scope | Typical technologies |
|---|---|---|
| Cluster and workload lifecycle | Declarative provisioning, onboarding, upgrades and GitOps reconciliation | Kubernetes, KRO, Azure Service Operator, Flux, Argo |
| Networking | CNI health, policy, ingress/egress, service connectivity and evidence | Cilium, Istio, Nginx, Traefik, network policy |
| Storage | Storage classes, claims, attachment/health evidence and workload boundaries | Persistent volumes, Longhorn and managed storage patterns |
| Security and identity | Workload identity, RBAC, policy, admission and least-privilege tool routes | OIDC, RBAC, Kyverno, Gatekeeper, Azure Policy |
| Observability | Metrics, logs, traces, dashboards, alerts and evidence correlation | Prometheus, Grafana, Alloy, Azure Monitor, Splunk, AppDynamics |
| Delivery | Repeatable changes, approvals, rollback and proof | GitOps, Flux, Argo Workflows/Events/Rollouts, CI/CD |

## GitOps-first platform factory

| Layer | Problem addressed | Demonstration in this repository |
|---|---|---|
| Cluster API | Large push pipelines duplicated orchestration and handled one environment at a time | A small KRO API composes ASO resource definitions; no Azure instance is included or applied |
| Pull reconciliation | Pipeline credentials and job ordering made delivery slow and fragile | Flux sources and ordered Kustomizations express continuous reconciliation, pruning and health waits |
| Team onboarding | Platform teams repeatedly hand-built namespaces and baseline controls | A locally runnable `TeamEnvironment` composes quota, limits, service account and default-deny networking |
| Secrets | Applications should not carry secret values through Git | External Secrets uses a fake synthetic provider here to demonstrate the contract without a real secret backend |
| Guardrails | Baseline ownership and security controls need consistent enforcement | A Kyverno policy requires accountable ownership on team namespaces |

The slice demonstrates the operator-based design and its consumer experience. The proof register distinguishes local reconciliation from definition-only integrations.

## AI integration platform

| Concern | Demonstration scope | Typical technologies |
|---|---|---|
| Agent composition | Bounded specialists and clear ownership; one synthetic specialist runs in the disposable demonstration | kagent, agent skills |
| Model and tool routing | One governed gateway for model, MCP and A2A traffic; OpenAI-compatible model routing is runtime-tested locally | agentgateway |
| Tool integration | Read-only and separately governed write paths | MCP, Kubernetes tools, data and observability tools |
| Agent collaboration | Typed hand-offs and evidence aggregation | A2A |
| Evaluation | Evidence, correctness, safety and usefulness gates | deterministic checks, lifecycle evaluations |
| Human authority | Review before consequential action | HITL, GitOps approval, workflow suspension |

## Business integration domains

- **Platform:** cluster lifecycle, networking, storage, identity, security, observability and developer enablement.
- **SRE:** incident triage, evidence correlation, diagnosis and bounded remediation proposals.
- **Compliance:** policy evidence collection, control mapping, exception explanation and human-owned sign-off.
- **Data:** governed retrieval, approved views/snapshots, schema-aware tools and explicit data classification.

The same platform pattern applies across the domains: allow-listed tools, bounded authority, evidence-rich outputs, evaluation, observability and human ownership.
