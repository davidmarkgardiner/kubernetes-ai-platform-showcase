# Case-study set

## 1. Kubernetes incident triage

**Problem:** platform incidents require evidence from Kubernetes events, networking, workloads and observability systems.

**Pattern:** kagent specialists gather evidence through read-only tools, exchange typed context through A2A and return a cited diagnosis and remediation proposal. agentgateway governs model and tool routing. Consequential action remains a separate approved GitOps workflow.

**Status:** delivered enterprise capability is described at outcome level; this repository publishes only the reusable pattern and safe reference implementation.

## 2. Platform engineering assistant

**Problem:** teams need consistent answers and onboarding across cluster lifecycle, networking, storage, identity, security and observability.

**Pattern:** a Kubernetes-first assistant routes questions to bounded domain skills, uses approved MCP tools for evidence, and produces runbook links or proposed GitOps changes. The Go policy gate demonstrates the read/write authority boundary.

**Status:** architecture and policy-gate demonstration implemented here; specific infrastructure backends remain environment-dependent.

## 3. Compliance evidence assistant

**Problem:** control owners spend time locating policy reports and translating technical evidence into reviewable control statements.

**Pattern:** read-only collectors retrieve allow-listed policy-shaped fixture evidence, the evidence router labels confidence and citations, and a human control owner approves the interpretation. Confidential export is denied by the example policy.

**Status:** the governed control pattern is implemented in this public reference; confidential production integrations and data are not published here.

## 4. Governed data assistant

**Problem:** business users need useful answers without giving an agent unrestricted database or production-table access.

**Pattern:** expose a supported API, approved database view/read replica, governed warehouse or versioned object-storage snapshot through a bounded tool contract. Limit schema, rows, result size and time. Record citations and data classification.

**Status:** evidence-routing and policy demonstration implemented here; source-specific connectors are intentionally absent.

## 5. Evidence-driven agentic delivery

**Problem:** coding agents can produce work quickly, but teams still need isolation, deterministic acceptance, independent review and release authority.

**Pattern:** approved work enters an isolated workspace, deterministic code owns the lifecycle, agents work inside bounded phases, and durable evidence records requested/actual routes, tests, reviews, PRs and CI. Merge and deployment remain policy-bound.

**Status:** supported by private delivery programmes; this repository is limited to reusable public-safe patterns and does not publish confidential run evidence.

## 6. GitOps-first cluster and application delivery

**Problem:** push-oriented CI/CD pipelines accumulated credentials and imperative orchestration, took too long to run and generally created or changed one cluster at a time. Application onboarding also required repeated platform-team intervention for namespaces and baseline controls.

**Pattern:** expose small KRO APIs backed by operator-owned resources. Azure Service Operator expresses the cloud resource graph; Flux continuously pulls cluster and application desired state; External Secrets separates secret references from workloads; Kyverno applies admission guardrails. A team request composes its namespace, quota, limits, service account and network boundary consistently.

**Value:** the pattern removes duplicated pipeline stages, supports parallel declarative reconciliation, corrects drift and turns onboarding into a reviewed Git change. It also gives the platform team one reusable control point instead of bespoke per-team work.

**Status:** the safe `TeamEnvironment` composition is runtime-tested in an isolated Kubernetes reference environment. The ASO, Flux, External Secrets and Kyverno integration manifests are structurally verified examples; confidential fleet configuration and cloud runtime evidence are not published here.
