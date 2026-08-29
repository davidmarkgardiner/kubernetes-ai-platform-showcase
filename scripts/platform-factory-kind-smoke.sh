#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cluster_name=platform-factory-showcase
receipt="$repo_root/evidence/runtime/platform-factory-kind-receipt.json"

cleanup() {
  kind delete cluster --name "$cluster_name" >/dev/null 2>&1 || true
}
trap cleanup EXIT

cleanup
kind create cluster --name "$cluster_name" --wait 120s

helm install kro oci://registry.k8s.io/kro/charts/kro \
  --namespace kro-system \
  --create-namespace \
  --version 0.9.3 \
  --set rbac.mode=aggregation \
  --wait \
  --timeout 5m

kubectl apply -f "$repo_root/platform-factory/rbac/kro-team-environment-role.yaml"
kubectl rollout restart deployment -n kro-system
kubectl rollout status deployment -n kro-system --timeout=180s
kubectl apply -f "$repo_root/platform-factory/definitions/team-environment.yaml"

for attempt in $(seq 1 60); do
  if kubectl get crd teamenvironments.platform.example.com >/dev/null 2>&1; then
    break
  fi
  if [ "$attempt" -eq 60 ]; then
    echo "TeamEnvironment CRD was not established" >&2
    exit 1
  fi
  sleep 2
done

kubectl wait --for=condition=Established crd/teamenvironments.platform.example.com --timeout=120s
kubectl apply -f "$repo_root/platform-factory/examples/team-environment.yaml"

for attempt in $(seq 1 60); do
  if kubectl get namespace team-demo >/dev/null 2>&1 && \
     kubectl get resourcequota team-budget -n team-demo >/dev/null 2>&1 && \
     kubectl get limitrange workload-defaults -n team-demo >/dev/null 2>&1 && \
     kubectl get serviceaccount workload -n team-demo >/dev/null 2>&1 && \
     kubectl get networkpolicy default-deny -n team-demo >/dev/null 2>&1; then
    break
  fi
  if [ "$attempt" -eq 60 ]; then
    echo "TeamEnvironment resources did not reconcile" >&2
    kubectl get resourcegraphdefinition team-environment -o yaml >&2 || true
    kubectl get teamenvironment demo-team -o yaml >&2 || true
    kubectl logs -n kro-system deployment/kro --tail=100 >&2 || true
    exit 1
  fi
  sleep 2
done

owner=$(kubectl get namespace team-demo -o jsonpath='{.metadata.labels.platform\.example\.com/owner}')
policy_types=$(kubectl get networkpolicy default-deny -n team-demo -o jsonpath='{.spec.policyTypes[*]}')
if [ "$owner" != "showcase" ]; then
  echo "unexpected namespace owner: $owner" >&2
  exit 1
fi
if [ "$policy_types" != "Ingress Egress" ]; then
  echo "unexpected default-deny policy types: $policy_types" >&2
  exit 1
fi

mkdir -p "$(dirname "$receipt")"
cat >"$receipt" <<JSON
{
  "schemaVersion": "1.0",
  "verifiedAt": "$(date -u +%Y-%m-%dT%H:%M:%SZ)",
  "cluster": "disposable-kind",
  "kroVersion": "0.9.3",
  "rbacMode": "aggregation",
  "result": "PASS",
  "observedResources": [
    "Namespace/team-demo",
    "ResourceQuota/team-demo/team-budget",
    "LimitRange/team-demo/workload-defaults",
    "ServiceAccount/team-demo/workload",
    "NetworkPolicy/team-demo/default-deny"
  ],
  "azureBlueprintApplied": false,
  "azureRuntime": "NOT_PROVEN",
  "fluxRuntime": "NOT_PROVEN",
  "externalSecretsRuntime": "NOT_PROVEN",
  "kyvernoRuntime": "NOT_PROVEN"
}
JSON

echo "PLATFORM_FACTORY_KIND_SMOKE_OK"
