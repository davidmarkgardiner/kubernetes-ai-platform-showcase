# Isolated kagent + agentgateway reference runtime

## Purpose

This bundle turns the architectural claim into a reproducible public integration test without using a commercial model key, employer environment or customer data.

```text
A2A client
  -> kagent safe-fixture specialist
  -> OpenAI-compatible ModelConfig
  -> agentgateway Gateway + HTTPRoute
  -> AgentgatewayPolicy prompt guard
  -> keyless httpbun mock model
  -> OpenTelemetry trace + token metrics
```

## Exact test boundary

- Kind provides the isolated Kubernetes reference environment.
- kagent `0.9.9` exposes one declarative A2A agent.
- agentgateway `1.4.0` owns the model route, policy and telemetry.
- The backend is a pinned httpbun image returning a deterministic OpenAI-shaped response.
- The allowed safe-fixture request completes through A2A.
- A request containing the blocked term is denied before the restricted route can run.
- The successful request produces a correlated trace and token-usage metrics.

Run:

```bash
./scripts/kind-demo-up.sh
./scripts/kind-demo-smoke.sh
./scripts/kind-demo-down.sh
```

## Troubleshooting evidence

The first integration attempt configured kagent as an Ollama client. That reached the gateway but called `/api/chat` and expected an Ollama response schema, so the A2A task failed validation. The corrected configuration uses kagent's OpenAI provider with its base URL pointed at agentgateway's OpenAI-compatible `/v1` endpoint. The successful smoke test covers that corrected path.

## Limitations

This proves component wiring, A2A transport, routing, policy denial and telemetry in an isolated public reference environment. It does not evaluate model reasoning, multi-cluster access, production availability, enterprise identity, persistent storage or a deployment in any employer/customer environment.

The component shape follows the official [kagent BYO Agentgateway guide](https://kagent.dev/docs/kagent/supported-providers/byo-agentgateway/) and [agentgateway Kubernetes installation guide](https://agentgateway.dev/docs/kubernetes/main/quickstart/install/).
