### For Go project

Command: `mkdir .claude && touch .claude/settings.local.json`

Then copy this content: 
```json
{
  "permissions": {
    "allow": [
      "Bash(go mod:*)",
      "Bash(go get:*)",
      "Bash(go test:*)",
      "Bash(go list:*)",
      "Bash(go build:*)",
      "Bash(make:*)",
      "Bash(golangci-lint:*)",
      "Bash(go tool pprof:*)",
      "WebFetch(domain:*)",
      "Bash(ls:*)",
      "Bash(cat:*)",
      "Bash(grep:*)"
    ],
    "deny": [
      "Bash(rm:*)",
      "Bash(git add:*)",
      "Bash(git commit:*)",
      "Bash(git push:*)",
      "Bash(go clean:*)",
      "Bash(sed -i:*)",
      "Bash(mv:*)"
    ]
  }
}
```
