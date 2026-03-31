### Install kubectl + helm Ubuntu
```bash
# kubectl
curl -LO "https://dl.k8s.io/release/$(curl -L -s https://dl.k8s.io/release/stable.txt)/bin/linux/amd64/kubectl"
sudo install -o root -g root -m 0755 kubectl /usr/local/bin/kubectl
kubectl version --client

# helm
curl -fsSL -o get_helm.sh https://raw.githubusercontent.com/helm/helm/main/scripts/get-helm-4
chmod 700 get_helm.sh
./get_helm.sh
```


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
