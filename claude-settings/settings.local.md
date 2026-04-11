### For Go project

Command: `mkdir .claude && touch .claude/settings.local.json`

Then copy this content: 
```json
{
  "permissions": {
    "allow": [
      "Read",
      "Edit",
      "Grep",
      "Glob",
      "Bash(go mod *)",
      "Bash(go get *)",
      "Bash(go test *)",
      "Bash(go list *)",
      "Bash(go build *)",
      "Bash(go mod tidy)",
      "Bash(go env *)",
      "Bash(go vet *)",
      "Bash(make test)",
      "Bash(make build)",
      "Bash(make lint)",
      "Bash(golangci-lint *)",
      "Bash(go tool pprof *)",
      "Bash(kubectl get *)",
      "Bash(kubectl describe *)",
      "Bash(kubectl logs *)",
      "Bash(kubectl top *)",
      "Bash(ls *)",
      "Bash(cat *)",
      "Bash(grep *)",
      "Bash(git status)",
      "Bash(git diff *)",
      "Bash(git log *)",
      "Bash(docker ps *)",
      "Bash(docker logs *)",
      "Bash(df *)",
      "Bash(free *)",
      "WebSearch",
      "WebFetch(domain:*)"
    ],
    "deny": [
      "Bash(rm *)",
      "Bash(mv *)",
      "Bash(git add *)",
      "Bash(git commit *)",
      "Bash(git push *)",
      "Bash(git reset *)",
      "Bash(go clean -modcache)",
      "Bash(go generate *)",
      "Bash(go install *)",
      "Bash(docker rm *)",
      "Bash(docker stop *)",
      "Bash(docker kill *)"
    ]
  },
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit|MultiEdit",
        "hooks": [
          {
            "type": "command",
            "command": "f=$(jq -r '.tool_input.file_path // empty' | grep '\\.go$'); if [ -n \"$f\" ] && [ -f \"$f\" ]; then (goimports -w \"$f\" 2>/dev/null || gofmt -w \"$f\") && (cd \"$(dirname \"$f\")\" && go vet ./... 2>&1 | head -10); fi || true",
            "timeout": 30,
            "statusMessage": "Refining Go code (fmt + vet)..."
          }
        ]
      }
    ],
    "PreCompact": [
      {
        "matcher": "auto|manual",
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"hookSpecificOutput\":{\"hookEventName\":\"PreCompact\",\"additionalContext\":\"GO PROJECT CONTEXT: 1. Use slog for structured logging. 2. Wrap errors using fmt.Errorf with %w. 3. Clean architecture: internal/ for logic, provider interfaces for external deps. 4. go mod tidy after adding deps. 5. Mocking: internal/provider/mock.go. 6. Table-driven tests. 7. Always propagate context.Context as first param.\"}}'",
            "timeout": 5
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "echo '{\"additionalContext\":\"Go: '$(go version 2>/dev/null | awk \"{print \\$3}\")' | Module: '$(head -1 go.mod 2>/dev/null | awk \"{print \\$2}\" || echo unknown)'\"}'",
            "timeout": 5
          }
        ]
      }
    ]
  }
}
```
