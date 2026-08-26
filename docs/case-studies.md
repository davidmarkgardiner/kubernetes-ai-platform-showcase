# Case-study set

## 1. Kubernetes incident triage

**Problem:** platform incidents require evidence from Kubernetes events, networking, workloads and observability systems.

**Pattern:** kagent specialists gather evidence through read-only tools, exchange typed context through A2A and return a cited diagnosis and remediation proposal. agentgateway governs model and tool routing. Consequential action remains a separate approved GitOps workflow.

**Status:** underlying patterns have existing sanitized and private evidence; this repository provides a curated demonstration, not a production claim.

## 2. Platform engineering assistant

**Problem:** teams need consistent answers and onboarding across cluster lifecycle, networking, storage, identity, security and observability.

**Pattern:** a Kubernetes-first assistant routes questions to bounded domain skills, uses approved MCP tools for evidence, and produces runbook links or proposed GitOps changes. The Go policy gate demonstrates the read/write authority boundary.

**Status:** architecture and policy-gate demonstration implemented here; specific infrastructure backends remain environment-dependent.

## 3. Compliance evidence assistant

**Problem:** control owners spend time locating policy reports and translating technical evidence into reviewable control statements.

**Pattern:** read-only collectors retrieve allow-listed synthetic policy evidence, the evidence router labels confidence and citations, and a human control owner approves the interpretation. Confidential export is denied by the example policy.

**Status:** synthetic cross-functional demonstration implemented here; no claim of a deployed compliance product.

## 4. Governed data assistant

**Problem:** business users need useful answers without giving an agent unrestricted database or production-table access.

**Pattern:** expose a supported API, approved database view/read replica, governed warehouse or versioned object-storage snapshot through a bounded tool contract. Limit schema, rows, result size and time. Record citations and data classification.

**Status:** evidence-routing and policy demonstration implemented here; source-specific connectors are intentionally absent.

## 5. Evidence-driven agentic delivery

**Problem:** coding agents can produce work quickly, but teams still need isolation, deterministic acceptance, independent review and release authority.

**Pattern:** approved work enters an isolated workspace, deterministic code owns the lifecycle, agents work inside bounded phases, and durable evidence records requested/actual routes, tests, reviews, PRs and CI. Merge and deployment remain policy-bound.

**Status:** supported by existing private working programmes; a future synthetic run receipt will be curated into this repository.
