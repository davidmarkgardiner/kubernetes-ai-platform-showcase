# Kubernetes + AI Platform Showcase

Private working repository for a concise, defensible demonstration of David Gardiner's Kubernetes and AI platform work.

This repository is intentionally broader than incident triage and intentionally not tied to one cloud. It shows how governed AI integrations can sit on top of Kubernetes platform capabilities across:

- platform engineering;
- SRE and incident response;
- compliance and control evidence;
- data access and governed retrieval.

## What is implemented

- A dependency-free **Go policy gate** that classifies read-only and consequential AI tool requests, enforces least privilege, requires human approval for mutation, and never executes the action itself.
- A dependency-free **Python evidence router** that validates synthetic findings, rejects secret-bearing or unsupported inputs, groups evidence by business domain, and labels confidence honestly.
- Synthetic examples for platform, SRE, compliance and data workflows.
- A plain hand-written HTML walkthrough at `demo/index.html`.
- A capability map and proof register that distinguish implemented, demonstrated, planned and environment-specific work.

## What this repository does not claim

- It is not an employer production repository.
- It does not contain employer data, customer data, credentials, internal endpoints or copied proprietary implementation.
- It does not claim autonomous production remediation.
- It does not claim every Kubernetes distribution, storage provider, CNI or business integration has the same runtime proof.
- It does not replace the original evidence sources; it curates a public-safe demonstration shape for later review.

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

See [the capability map](docs/capability-map.md), [case studies](docs/case-studies.md) and [proof register](docs/proof-register.md).
