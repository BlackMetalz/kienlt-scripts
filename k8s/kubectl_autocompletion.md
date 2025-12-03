### Zsh
```
# Kubectl autocompletion
alias k="kubectl"
source <(kubectl completion zsh)
# Helm auto complete
source <(helm completion zsh)
```

### Bash
```bash
alias k=kubectl
source <(kubectl completion bash)
complete -F __start_kubectl k
# Helm auto complete
source <(helm completion bash)
```
