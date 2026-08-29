# GitOps platform factory

This slice demonstrates the shape of a pull-based Kubernetes platform factory without copying an employer implementation or containing live cloud configuration.

It separates two proof levels deliberately:

- `definitions/team-environment.yaml` is safe to exercise in an isolated reference cluster. It composes a namespace, quota, limits, service account and default-deny network policy from one small developer-facing API.
- `definitions/aks-cluster-blueprint.yaml` is a definition-only example showing how KRO can compose Azure Service Operator resources. There is no `AzureKubernetesCluster` instance in this repository, and the verification scripts never apply this definition.
- `gitops/` shows Flux source, ordering and Helm reconciliation with an inert example repository URL.
- `addons/` shows External Secrets with its public-safe fake provider and a Kyverno ownership policy.

## Problem this pattern solves

Push pipelines often carry cloud credentials, encode orchestration in job stages and create one cluster or workload environment at a time. This pattern moves desired state into Git and lets controllers reconcile it continuously. The platform team owns the compositions and policy; consumers submit small, reviewed custom resources.

The expected operational value is shorter onboarding, less pipeline duplication, consistent guardrails, drift correction and a clearer audit trail. Those are architectural outcomes here, not measured production claims.

## Verification

Run the structural, safety and proof-boundary checks:

```bash
python3 scripts/verify-platform-factory.py
```

Run the safe KRO composition in the isolated reference environment:

```bash
./scripts/platform-factory-kind-smoke.sh
```

The reference smoke test installs KRO with aggregation-mode RBAC and grants only the resource permissions needed by `TeamEnvironment`. It never installs Azure Service Operator, never applies the Azure blueprint and never contacts Azure.

## Deliberate limitations

- Azure provisioning is structurally demonstrated, not runtime-proven here.
- Flux, External Secrets and Kyverno manifests are structurally validated, not reconciled by their controllers here.
- The example Git URL and all secret data are public-safe placeholders.
- Creating cloud infrastructure remains a separate, explicitly authorised action outside this repository.
