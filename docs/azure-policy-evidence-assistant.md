# Azure Policy compliance evidence assistant

Status: **implemented and tested locally with synthetic fixtures**

This reference workflow demonstrates how a forward-deployed AI integration can be made governable before a model or live platform is introduced. A deterministic local engine reads Azure Policy-shaped fixtures through a static gateway, records provenance, denies a planned remediation attempt, and produces a repeatable evidence bundle.

It is deliberately model-free and cloud-free. It does not use Azure, Azure Policy, Entra, kagent, agentgateway or Microsoft Task Adherence. Those products inform the workflow shape; the implementation proves only its local controls.

## Safety and proof contract

- closed, synthetic fixtures and resolvable references;
- explicit fixture identity and exact scope checks;
- pre-dispatch plan comparison;
- static tool allowlist outside fixture control;
- adapters exposing read methods only;
- denied writes recorded before adapter invocation;
- deterministic evidence and trace files;
- negative tests for adapter bypass, identity forgery, scope escalation and allowlist injection.

Run:

```bash
python3 -m policy_evidence.cli
python3 -m unittest tests.test_policy_evidence
```

Generated files stay under `policy_evidence/out/` and are not a live-tenant receipt. See `evidence/policy-evidence-receipt.json` for the executed local test status and explicit limitations.
