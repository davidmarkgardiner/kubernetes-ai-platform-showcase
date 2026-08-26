#!/usr/bin/env bash
set -euo pipefail

cluster_name="kubernetes-ai-showcase"

if kind get clusters | grep -Fxq "$cluster_name"; then
  kind delete cluster --name "$cluster_name"
else
  echo "cluster ${cluster_name} is not present"
fi
