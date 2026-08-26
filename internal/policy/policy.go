package policy

import (
	"fmt"
	"slices"
	"strings"
)

var allowedDomains = []string{"platform", "sre", "compliance", "data"}
var readOnlyActions = []string{"inspect", "list", "query", "explain", "summarise"}
var consequentialActions = []string{"apply", "deploy", "delete", "modify", "write", "export"}

type Request struct {
	ID                 string `json:"id"`
	Domain             string `json:"domain"`
	Action             string `json:"action"`
	Resource           string `json:"resource"`
	DataClassification string `json:"data_classification"`
	ToolMode           string `json:"tool_mode"`
	HumanApproved      bool   `json:"human_approved"`
}

type Decision struct {
	RequestID           string   `json:"request_id"`
	Decision            string   `json:"decision"`
	ExecutionAuthorized bool     `json:"execution_authorized"`
	Reasons             []string `json:"reasons"`
	Requirements        []string `json:"requirements,omitempty"`
}

func Evaluate(req Request) Decision {
	req.Domain = strings.ToLower(strings.TrimSpace(req.Domain))
	req.Action = strings.ToLower(strings.TrimSpace(req.Action))
	req.ToolMode = strings.ToLower(strings.TrimSpace(req.ToolMode))
	req.DataClassification = strings.ToLower(strings.TrimSpace(req.DataClassification))

	decision := Decision{RequestID: req.ID, Decision: "deny", ExecutionAuthorized: false}

	if strings.TrimSpace(req.ID) == "" || strings.TrimSpace(req.Resource) == "" {
		decision.Reasons = []string{"request id and resource are required"}
		return decision
	}
	if !slices.Contains(allowedDomains, req.Domain) {
		decision.Reasons = []string{fmt.Sprintf("domain %q is not allow-listed", req.Domain)}
		return decision
	}

	if slices.Contains(readOnlyActions, req.Action) {
		if req.ToolMode != "read-only" {
			decision.Reasons = []string{"read-only work must use a read-only tool route"}
			decision.Requirements = []string{"select an allow-listed read-only tool"}
			return decision
		}
		decision.Decision = "allow-read-only"
		decision.Reasons = []string{"domain and action are allow-listed", "least-privilege tool mode is satisfied"}
		return decision
	}

	if slices.Contains(consequentialActions, req.Action) {
		if req.Action == "export" && slices.Contains([]string{"restricted", "confidential"}, req.DataClassification) {
			decision.Reasons = []string{"export of restricted or confidential data is prohibited by this demonstration policy"}
			return decision
		}
		if req.ToolMode != "write-capable" {
			decision.Reasons = []string{"requested action is unavailable through the selected tool route"}
			decision.Requirements = []string{"use a separately governed write-capable workflow"}
			return decision
		}
		decision.Decision = "review-required"
		decision.Reasons = []string{"consequential action cannot be executed directly by this gate"}
		decision.Requirements = []string{"approved workflow service account", "change evidence", "rollback plan", "independent human approval"}
		if req.HumanApproved {
			decision.Reasons = append(decision.Reasons, "human approval is recorded, but execution remains external to this gate")
		}
		return decision
	}

	decision.Reasons = []string{fmt.Sprintf("action %q is not recognised", req.Action)}
	return decision
}
