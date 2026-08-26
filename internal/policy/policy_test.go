package policy

import "testing"

func TestReadOnlyPlatformQueryAllowed(t *testing.T) {
	got := Evaluate(Request{ID: "req-1", Domain: "platform", Action: "query", Resource: "cluster-health", ToolMode: "read-only"})
	if got.Decision != "allow-read-only" || got.ExecutionAuthorized {
		t.Fatalf("unexpected decision: %#v", got)
	}
}

func TestWriteActionRequiresExternalReview(t *testing.T) {
	got := Evaluate(Request{ID: "req-2", Domain: "sre", Action: "apply", Resource: "deployment/example", ToolMode: "write-capable", HumanApproved: true})
	if got.Decision != "review-required" || got.ExecutionAuthorized {
		t.Fatalf("unexpected decision: %#v", got)
	}
}

func TestConfidentialExportDenied(t *testing.T) {
	got := Evaluate(Request{ID: "req-3", Domain: "compliance", Action: "export", Resource: "control-evidence", ToolMode: "write-capable", DataClassification: "confidential", HumanApproved: true})
	if got.Decision != "deny" || got.ExecutionAuthorized {
		t.Fatalf("unexpected decision: %#v", got)
	}
}

func TestUnknownDomainDenied(t *testing.T) {
	got := Evaluate(Request{ID: "req-4", Domain: "unknown", Action: "query", Resource: "anything", ToolMode: "read-only"})
	if got.Decision != "deny" {
		t.Fatalf("unexpected decision: %#v", got)
	}
}
