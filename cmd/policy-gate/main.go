package main

import (
	"encoding/json"
	"fmt"
	"io"
	"os"

	"github.com/davidmarkgardiner/kubernetes-ai-platform-showcase/internal/policy"
)

func main() {
	var input io.Reader = os.Stdin
	if len(os.Args) > 2 {
		fmt.Fprintln(os.Stderr, "usage: policy-gate [request.json]")
		os.Exit(2)
	}
	if len(os.Args) == 2 {
		file, err := os.Open(os.Args[1])
		if err != nil {
			fmt.Fprintln(os.Stderr, err)
			os.Exit(1)
		}
		defer file.Close()
		input = file
	}

	var request policy.Request
	decoder := json.NewDecoder(input)
	decoder.DisallowUnknownFields()
	if err := decoder.Decode(&request); err != nil {
		fmt.Fprintln(os.Stderr, "invalid request:", err)
		os.Exit(1)
	}

	output, err := json.MarshalIndent(policy.Evaluate(request), "", "  ")
	if err != nil {
		fmt.Fprintln(os.Stderr, err)
		os.Exit(1)
	}
	fmt.Println(string(output))
}
