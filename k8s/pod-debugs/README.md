### Some useful pod for testing
```
kubectl run curl-test --image=curlimages/curl -- /bin/sh -c "sleep infinity"

kubectl run test-tools --image=busybox -- /bin/sh -c "sleep infinity"

kubectl run dig-test --image=tutum/dnsutils -- /bin/sh -c "sleep infinity"
```

### Dockerfile for kienlt992/linux-tools
```
# Use Alpine as the base image
FROM alpine:latest

# Switch to root user
USER root

# Install bind-tools, curl, MySQL client, and Redis client
RUN apk add --no-cache bind-tools curl mysql-client redis

# Default command to keep the container running
CMD ["sleep", "infinity"]
```

- Build: docker build -t kienlt992/linux-tools:latest .

Usage:
- Docker: `docker run -d --name linux-tools kienlt992/linux-tools`
- K8s: `kubectl run kienlt-linux-tools --image=kienlt992/linux-tools`
