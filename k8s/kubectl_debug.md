### Useful for managed cluster
- Pods are starting evicted, the reason is disk pressure. We can't ssh into server because it is fucking managed service.
- Solution: Use `kubectl debug`. So assume I know where is the path take the most disk usage.
```bash
NODE=<node-name-here-bro>
# du command
kubectl debug node/$NODE -it --image=alpine -- chroot /host sh -c 'du -sh /opt/k8s-volumes/voicebot* 2>/dev/null | sort -h | tail -20'
# ls command
kubectl debug node/$NODE -it --image=alpine -- chroot /host sh -c 'ls -l /opt/k8s-volumes/* 2>/dev/null | sort -h | tail -20'
```

### Manifest for pod debug
```yaml
  # debug-pod.yaml
  apiVersion: v1
  kind: Pod
  metadata:
    name: debug-pod
    namespace: default
  spec:
    nodeName: <NODE-NAME>      # ép schedule lên đúng node
    hostPID: true
    hostNetwork: true
    priorityClassName: system-node-critical
    tolerations:
    - operator: Exists          # tolerate hết taint, kể cả disk-pressure
    containers:
    - name: scan
      image: alpine
      command: ["sleep", "3600"]
      securityContext:
        privileged: true
      volumeMounts:
      - name: host
        mountPath: /host
    volumes:
    - name: host
      hostPath:
        path: /
    restartPolicy: Never
```

Exec into post, now `/opt` folder will be `/host/opt`. +1 experience when debug xD