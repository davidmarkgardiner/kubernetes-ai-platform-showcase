# Kubernetes + AI Platform Showcase

Public-safe reference implementation of enterprise Kubernetes platform engineering and governed AI integration patterns.

Licensed under the [Apache License 2.0](LICENSE).

This repository is intentionally broader than incident triage and intentionally not tied to one cloud. It shows how governed AI integrations can sit on top of Kubernetes platform capabilities across:

- platform engineering;
- SRE and incident response;
- compliance and control evidence;
- data access and governed retrieval.

The repository makes reusable architecture, controls and verification paths reviewable without publishing confidential employer or customer implementation. Public receipts validate the reference implementation only; production delivery evidence remains private.

## What is implemented in the public reference

- A dependency-free **Go policy gate** that classifies read-only and consequential AI tool requests, enforces least privilege, requires human approval for mutation, and never executes the action itself.
- A dependency-free **Python evidence router** that validates safe fixture findings, rejects secret-bearing or unsupported inputs, groups evidence by business domain, and labels confidence honestly.
- An isolated **Kubernetes reference runtime** connecting kagent to agentgateway through an OpenAI-compatible route, with a keyless model substitute, request controls, OpenTelemetry traces and token metrics.
- A sanitised **GitOps platform-factory slice** showing KRO compositions, Azure Service Operator resource definitions, Flux reconciliation, External Secrets and Kyverno guardrails without cloud credentials or a provisionable cluster instance.
- A second isolated reference proof for the safe self-service path: one `TeamEnvironment` request reconciles a namespace, quota, limits, workload service account and default-deny network policy.
- Public-safe examples for platform, SRE, compliance and data workflows.
- A plain hand-written HTML walkthrough at `demo/index.html`.
- A capability map and proof register that distinguish implemented, demonstrated, planned and environment-specific work.
- A deterministic, model-free **Azure Policy compliance evidence assistant** that validates closed safe fixtures, enforces identity and scope through a static read-only gateway, records a planned write denial, and emits repeatable evidence and traces.

## What this repository does not claim

- It is not copied from an employer or customer production repository.
- It does not contain employer data, customer data, credentials, internal endpoints or copied proprietary implementation.
- It does not claim autonomous production remediation.
- It does not claim every Kubernetes distribution, storage provider, CNI or business integration has the same runtime proof.
- It does not replace confidential production evidence; it provides a public-safe, reproducible reference for technical review.

## Quick verification

```bash
./scripts/verify.sh
```

Run the Go policy gate:

```bash
go run ./cmd/policy-gate ./examples/requests/platform-read.json
go run ./cmd/policy-gate ./examples/requests/compliance-export.json
```

Run the Python evidence router:

```bash
python3 tools/evidence_router.py examples/evidence/synthetic-findings.json
```

Run the Azure Policy-shaped evidence reference workflow:

```bash
python3 -m policy_evidence.cli
python3 -m unittest tests.test_policy_evidence
```

This isolated reference does not connect to Azure or use an LLM. Its receipt records the exact controls exercised and keeps enforced no-network isolation as `NOT_PROVEN`.

Run the isolated Kubernetes reference environment:

```bash
./scripts/kind-demo-up.sh
./scripts/kind-demo-smoke.sh
./scripts/kind-demo-down.sh
```

The smoke test writes a sanitized receipt to `evidence/runtime/kind-showcase-receipt.json`. It validates the public integration path and control/telemetry behaviour without exposing production systems or data. The first setup may take several minutes while images and charts are fetched.

Verify the GitOps platform-factory definitions:

```bash
python3 scripts/verify-platform-factory.py
```

Reproduce the runtime-tested KRO team-onboarding composition in the isolated reference environment:

```bash
./scripts/platform-factory-kind-smoke.sh
```

This path never applies the Azure blueprint. Azure provisioning and Flux, External Secrets and Kyverno controller reconciliation remain explicitly outside that public receipt.

Open the walkthrough:

```bash
open demo/index.html
```

## Delivery model

The operating model is deliberately simple:

1. **Discover** the workflow, owner, data and success measure.
2. **Design** the AI, deterministic and human boundaries.
3. **Deliver** the smallest useful integration through Kubernetes and GitOps.
4. **Evaluate** correctness, evidence quality, safety and operational value.
5. **Adopt** with observability, onboarding, rollback and clear ownership.

See [the capability map](docs/capability-map.md), [case studies](docs/case-studies.md), [GitOps platform factory](platform-factory/README.md), [runtime demonstration](docs/runtime-demo.md) and [proof register](docs/proof-register.md).
