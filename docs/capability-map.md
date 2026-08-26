# Capability map

## Kubernetes platform engineering

The positioning is Kubernetes-first rather than cloud-first. AKS is one substantial delivery environment, alongside experience with self-managed and other managed Kubernetes platforms.

| Platform concern | Demonstration scope | Typical technologies |
|---|---|---|
| Cluster and workload lifecycle | Declarative provisioning, onboarding, upgrades and GitOps reconciliation | Kubernetes, KRO, Azure Service Operator, Flux, Argo |
| Networking | CNI health, policy, ingress/egress, service connectivity and evidence | Cilium, Istio, Nginx, Traefik, network policy |
| Storage | Storage classes, claims, attachment/health evidence and workload boundaries | CSI, persistent volumes, Longhorn and managed storage patterns |
| Security and identity | Workload identity, RBAC, policy, admission and least-privilege tool routes | OIDC, RBAC, Kyverno, Gatekeeper, Azure Policy |
| Observability | Metrics, logs, traces, dashboards, alerts and evidence correlation | Prometheus, Grafana, Alloy, Azure Monitor, Splunk, AppDynamics |
| Delivery | Repeatable changes, approvals, rollback and proof | GitOps, Flux, Argo Workflows/Events/Rollouts, CI/CD |

## AI integration platform

| Concern | Demonstration scope | Typical technologies |
|---|---|---|
| Agent composition | Bounded specialists and clear ownership | kagent, agent skills |
| Model and tool routing | One governed gateway for model, MCP and A2A traffic | agentgateway |
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
