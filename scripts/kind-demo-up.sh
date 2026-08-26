#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

cluster_name="kubernetes-ai-showcase"
context="kind-${cluster_name}"
node_image="kindest/node@sha256:452d707d4862f52530247495d180205e029056831160e22870e37e3f6c1ac31f"
gateway_api_version="1.6.0"
agentgateway_version="1.4.0"
kagent_version="0.9.9"
otel_chart_version="0.127.2"

for binary in docker kind kubectl helm curl jq; do
  command -v "$binary" >/dev/null 2>&1 || {
    echo "missing required binary: ${binary}" >&2
    exit 1
  }
done

docker info >/dev/null

if ! kind get clusters | grep -Fxq "$cluster_name"; then
  kind create cluster \
    --name "$cluster_name" \
    --image "$node_image" \
    --config deploy/kind/kind-config.yaml
fi

kubectl --context "$context" cluster-info >/dev/null

kubectl --context "$context" apply --server-side -f \
  "https://github.com/kubernetes-sigs/gateway-api/releases/download/v${gateway_api_version}/standard-install.yaml"

helm upgrade --install agentgateway-crds \
  oci://cr.agentgateway.dev/charts/agentgateway-crds \
  --version "$agentgateway_version" \
  --namespace agentgateway-system \
  --create-namespace \
  --kube-context "$context" \
  --wait

helm upgrade --install agentgateway \
  oci://cr.agentgateway.dev/charts/agentgateway \
  --version "$agentgateway_version" \
  --namespace agentgateway-system \
  --kube-context "$context" \
  --wait

helm upgrade --install opentelemetry-collector-traces opentelemetry-collector \
  --repo https://open-telemetry.github.io/opentelemetry-helm-charts \
  --version "$otel_chart_version" \
  --namespace telemetry \
  --create-namespace \
  --kube-context "$context" \
  --values deploy/kind/otel-traces-values.yaml \
  --wait

kubectl --context "$context" apply -f deploy/kind/httpbun.yaml
kubectl --context "$context" rollout status deployment/httpbun -n showcase-model --timeout=180s
kubectl --context "$context" apply -f deploy/kind/agentgateway.yaml
kubectl --context "$context" wait --for=condition=Programmed \
  gateway/agentgateway-proxy -n agentgateway-system --timeout=180s
kubectl --context "$context" wait --for=condition=Available \
  deployment/agentgateway-proxy -n agentgateway-system --timeout=180s
for _ in $(seq 1 60); do
  if kubectl --context "$context" get httproute synthetic-llm -n agentgateway-system -o json |
    jq -e '[.status.parents[].conditions[] | select(.type == "Accepted" and .status == "True")] | length > 0' \
      >/dev/null; then
    break
  fi
  sleep 2
done
kubectl --context "$context" get httproute synthetic-llm -n agentgateway-system -o json |
  jq -e '[.status.parents[].conditions[] | select(.type == "Accepted" and .status == "True")] | length > 0' \
    >/dev/null

helm upgrade --install kagent-crds \
  oci://ghcr.io/kagent-dev/kagent/helm/kagent-crds \
  --version "$kagent_version" \
  --namespace kagent \
  --create-namespace \
  --kube-context "$context" \
  --set kmcp.enabled=false \
  --wait

helm upgrade --install kagent \
  oci://ghcr.io/kagent-dev/kagent/helm/kagent \
  --version "$kagent_version" \
  --namespace kagent \
  --kube-context "$context" \
  --values deploy/kind/kagent-values.yaml \
  --wait \
  --timeout 10m

kubectl --context "$context" apply -f deploy/kind/kagent-model.yaml
kubectl --context "$context" wait --for=condition=Accepted \
  modelconfig/agentgateway-synthetic-model -n kagent --timeout=180s
kubectl --context "$context" apply -f deploy/kind/kagent-agent.yaml
kubectl --context "$context" wait --for=condition=Ready \
  agent/platform-evidence-specialist -n kagent --timeout=8m

echo "SHOWCASE_CLUSTER_READY context=${context} agentgateway=${agentgateway_version} kagent=${kagent_version}"
