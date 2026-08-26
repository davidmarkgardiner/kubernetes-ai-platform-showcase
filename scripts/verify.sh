#!/usr/bin/env bash
set -euo pipefail

repo_root=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
cd "$repo_root"

go test ./...
python3 -m unittest discover -s tests -p 'test_*.py'
python3 tools/evidence_router.py examples/evidence/synthetic-findings.json >/dev/null
go run ./cmd/policy-gate ./examples/requests/platform-read.json | grep -q 'allow-read-only'
go run ./cmd/policy-gate ./examples/requests/compliance-export.json | grep -q '"decision": "deny"'

if rg -n --hidden --glob '!.git/**' '(BEGIN (RSA |EC |OPENSSH )?PRIVATE KEY|ghp_[A-Za-z0-9]{20,}|sk-[A-Za-z0-9]{20,}|AKIA[0-9A-Z]{16})' .; then
  echo 'secret-like material detected' >&2
  exit 1
fi

if rg -n --hidden --glob '!.git/**' '(subscription[_ -]?id|tenant[_ -]?id)[[:space:]]*[:=][[:space:]]*[0-9a-fA-F-]{30,}' .; then
  echo 'cloud identifier detected' >&2
  exit 1
fi

echo 'SHOWCASE_VERIFY_OK'
