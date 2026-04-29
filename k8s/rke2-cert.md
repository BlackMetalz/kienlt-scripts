### Restart rotation
- Rotate cert by restart service in rke2.
- Remember restart in `rke2-server` in master node first before restart `rke2-agent` in worker node
- Restart one by one. After every restart, check node status before continue.

### Check cert in Agent
```bash
for f in /var/lib/rancher/rke2/agent/*.crt; do
    echo "=== $f ==="
    openssl x509 -in "$f" -noout -subject -dates 2>/dev/null
done
```

### Check cert in Server
```bash
  for f in /var/lib/rancher/rke2/server/tls/*.crt /var/lib/rancher/rke2/server/tls/etcd/*.crt; do
    echo "=== $f ==="
    openssl x509 -in "$f" -noout -subject -dates 2>/dev/null
  done
```