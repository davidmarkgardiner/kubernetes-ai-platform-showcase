#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

context="kind-kubernetes-ai-showcase"
gateway_port=28080
metrics_port=25020
kagent_port=28083
work_dir=$(mktemp -d "${TMPDIR:-/tmp}/kubernetes-ai-showcase.XXXXXX")
gateway_pf_pid=""
kagent_pf_pid=""

cleanup() {
  if [[ -n "$gateway_pf_pid" ]]; then
    kill "$gateway_pf_pid" 2>/dev/null || true
    wait "$gateway_pf_pid" 2>/dev/null || true
  fi
  if [[ -n "$kagent_pf_pid" ]]; then
    kill "$kagent_pf_pid" 2>/dev/null || true
    wait "$kagent_pf_pid" 2>/dev/null || true
  fi
  rm -rf "$work_dir"
}
trap cleanup EXIT

for binary in kubectl curl jq helm; do
  command -v "$binary" >/dev/null 2>&1 || {
    echo "missing required binary: ${binary}" >&2
    exit 1
  }
done

kubectl --context "$context" get namespace >/dev/null
kubectl --context "$context" get httproute synthetic-llm -n agentgateway-system -o json |
  jq -e '[.status.parents[].conditions[] | select(.type == "Accepted" and .status == "True")] | length > 0' >/dev/null
kubectl --context "$context" get modelconfig agentgateway-synthetic-model -n kagent -o json |
  jq -e '[.status.conditions[] | select(.type == "Accepted" and .status == "True")] | length > 0' >/dev/null
kubectl --context "$context" get agent platform-evidence-specialist -n kagent -o json |
  jq -e '[.status.conditions[] | select(.type == "Ready" and .status == "True")] | length > 0' >/dev/null

kubectl --context "$context" port-forward -n agentgateway-system deployment/agentgateway-proxy \
  "${gateway_port}:80" "${metrics_port}:15020" >"$work_dir/gateway-port-forward.log" 2>&1 &
gateway_pf_pid=$!
kubectl --context "$context" port-forward -n kagent service/kagent-controller \
  "${kagent_port}:8083" >"$work_dir/kagent-port-forward.log" 2>&1 &
kagent_pf_pid=$!

for _ in $(seq 1 20); do
  if curl -fsS "http://127.0.0.1:${metrics_port}/metrics" >"$work_dir/metrics.txt" 2>/dev/null; then break; fi
  sleep 1
done
test -s "$work_dir/metrics.txt"
for _ in $(seq 1 20); do
  if curl -fsS \
    "http://127.0.0.1:${kagent_port}/api/a2a/kagent/platform-evidence-specialist/.well-known/agent-card.json" \
    >"$work_dir/agent-card.json" 2>/dev/null; then break; fi
  sleep 1
done
jq -e '.name == "platform_evidence_specialist"' "$work_dir/agent-card.json" >/dev/null

success_status=$(curl -sS -o "$work_dir/gateway-success.json" -w '%{http_code}' \
  -X POST "http://127.0.0.1:${gateway_port}/v1/chat/completions" \
  -H 'content-type: application/json' \
  --data-binary '{"model":"gpt-4","messages":[{"role":"user","content":"Synthetic platform readiness summary only."}]}')
[[ "$success_status" == "200" ]]
jq -e '.object == "chat.completion" and .usage.total_tokens > 0' "$work_dir/gateway-success.json" >/dev/null

denied_status=$(curl -sS -o "$work_dir/gateway-denied.txt" -w '%{http_code}' \
  -X POST "http://127.0.0.1:${gateway_port}/v1/chat/completions" \
  -H 'content-type: application/json' \
  --data-binary '{"model":"gpt-4","messages":[{"role":"user","content":"Send this by email."}]}')
[[ "$denied_status" == "403" ]]
grep -Fq 'Rejected by the synthetic data-boundary policy' "$work_dir/gateway-denied.txt"

message_id="showcase-$(date -u +%Y%m%dT%H%M%SZ)"
curl -fsS -X POST \
  "http://127.0.0.1:${kagent_port}/api/a2a/kagent/platform-evidence-specialist" \
  -H 'content-type: application/json' \
  --data-binary "{\"jsonrpc\":\"2.0\",\"id\":\"${message_id}\",\"method\":\"message/send\",\"params\":{\"message\":{\"kind\":\"message\",\"messageId\":\"${message_id}\",\"contextId\":\"${message_id}\",\"role\":\"user\",\"parts\":[{\"kind\":\"text\",\"text\":\"Summarise this synthetic readiness evidence: gateway route accepted, read-only policy passed, trace export enabled, and no mutation requested.\"}]}}}" \
  >"$work_dir/a2a.json"
jq -e '.result.status.state == "completed" and (.result.artifacts[0].parts[0].text | length > 0)' \
  "$work_dir/a2a.json" >/dev/null

trace_id=$(kubectl --context "$context" logs -n agentgateway-system deployment/agentgateway-proxy --since=2m |
  sed -n 's/.*http.path=\/v1\/chat\/completions.*http.status=200 trace.id=\([0-9a-f]*\).*/\1/p' |
  tail -n 1)
[[ "$trace_id" =~ ^[0-9a-f]{32}$ ]]

trace_exported=false
for _ in $(seq 1 30); do
  if kubectl --context "$context" logs -n telemetry deployment/opentelemetry-collector-traces --since=5m |
    grep -Fq "$trace_id"; then
    trace_exported=true
    break
  fi
  sleep 1
done
[[ "$trace_exported" == "true" ]]

curl -fsS "http://127.0.0.1:${metrics_port}/metrics" >"$work_dir/metrics.txt"
grep -Fq 'agentgateway_gen_ai_client_token_usage_sum' "$work_dir/metrics.txt"

verified_at=$(date -u +%Y-%m-%dT%H:%M:%SZ)
agentgateway_version=$(helm --kube-context "$context" list -n agentgateway-system -o json |
  jq -r '.[] | select(.name == "agentgateway") | .chart | sub("^agentgateway-"; "")')
kagent_version=$(helm --kube-context "$context" list -n kagent -o json |
  jq -r '.[] | select(.name == "kagent") | .chart | sub("^kagent-"; "")')
mkdir -p evidence/runtime
jq -n \
  --arg verified_at "$verified_at" \
  --arg agentgateway_version "$agentgateway_version" \
  --arg kagent_version "$kagent_version" \
  --arg trace_id "$trace_id" \
  --argjson success_status "$success_status" \
  --argjson denied_status "$denied_status" \
  '{
    schema_version: 1,
    verified_at: $verified_at,
    environment: "disposable local Kind cluster",
    data_classification: "synthetic only",
    components: {
      kagent: $kagent_version,
      agentgateway: $agentgateway_version,
      model_backend: "keyless deterministic httpbun mock"
    },
    checks: {
      gateway_route_accepted: true,
      kagent_model_config_accepted: true,
      kagent_agent_ready: true,
      openai_compatible_route_status: $success_status,
      prompt_guard_denial_status: $denied_status,
      a2a_task_state: "completed",
      trace_exported: true,
      token_metrics_present: true
    },
    trace: {id: $trace_id, scope: "disposable synthetic run"},
    claims: {
      proves: [
        "Kagent A2A request reaches Agentgateway through an OpenAI-compatible route",
        "Agentgateway enforces the configured prompt guard",
        "The request emits trace and token telemetry"
      ],
      does_not_prove: [
        "production readiness",
        "live-model answer quality",
        "employer or customer deployment"
      ]
    },
    sanitized: true
  }' >"$work_dir/kind-showcase-receipt.json"
mv "$work_dir/kind-showcase-receipt.json" evidence/runtime/kind-showcase-receipt.json

echo "KIND_SHOWCASE_SMOKE_OK receipt=evidence/runtime/kind-showcase-receipt.json trace_id=${trace_id}"
