# Install Redis cluster fast without a storage class in 3 node lab environment

**For lab only! Who the fuck uses this for prod? xD**

```bash
NAME    STATUS   ROLES           AGE   VERSION
node1   Ready    control-plane   11d   v1.34.2
node2   Ready    control-plane   11d   v1.34.2
node3   Ready    control-plane   11d   v1.34.2
```

- Create 3 folders in 3 nodes
```bash
# Node 1
/var/lib/redis-cluster/redis-0
# Node 2
/var/lib/redis-cluster/redis-1
# Node 3
/var/lib/redis-cluster/redis-2
```

- Apply this fucking manifest: `redis-cluster-lab.yaml`
```yaml
apiVersion: v1
kind: Namespace
metadata:
  name: redis-lab
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: redis-config
  namespace: redis-lab
data:
  redis.conf: |
    port 6379
    bind 0.0.0.0
    protected-mode no

    dir /data
    dbfilename dump.rdb

    cluster-enabled yes
    cluster-config-file /data/nodes.conf
    cluster-node-timeout 5000

    appendonly yes
    appendfsync everysec

    save 300 100
    save 60 1000

    logfile ""
---
apiVersion: v1
kind: Service
metadata:
  name: redis-0
  namespace: redis-lab
spec:
  clusterIP: None
  publishNotReadyAddresses: true
  selector:
    statefulset.kubernetes.io/pod-name: redis-0-0
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
    - name: cluster-bus
      port: 16379
      targetPort: 16379
---
apiVersion: v1
kind: Service
metadata:
  name: redis-1
  namespace: redis-lab
spec:
  clusterIP: None
  publishNotReadyAddresses: true
  selector:
    statefulset.kubernetes.io/pod-name: redis-1-0
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
    - name: cluster-bus
      port: 16379
      targetPort: 16379
---
apiVersion: v1
kind: Service
metadata:
  name: redis-2
  namespace: redis-lab
spec:
  clusterIP: None
  publishNotReadyAddresses: true
  selector:
    statefulset.kubernetes.io/pod-name: redis-2-0
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
    - name: cluster-bus
      port: 16379
      targetPort: 16379
---
apiVersion: v1
kind: Service
metadata:
  name: redis
  namespace: redis-lab
spec:
  selector:
    app: redis
  ports:
    - name: redis
      port: 6379
      targetPort: 6379
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-0
  namespace: redis-lab
spec:
  serviceName: redis-0
  replicas: 1
  selector:
    matchLabels:
      app: redis
      instance: redis-0
  template:
    metadata:
      labels:
        app: redis
        instance: redis-0
    spec:
      nodeName: node1
      tolerations:
        - key: node-role.kubernetes.io/control-plane
          operator: Exists
          effect: NoSchedule
      terminationGracePeriodSeconds: 30
      containers:
        - name: redis
          image: redis:7.2
          imagePullPolicy: IfNotPresent
          env:
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          command:
            - sh
            - -c
            - |
              cp /conf/redis.conf /tmp/redis.conf
              echo "cluster-announce-ip ${POD_IP}" >> /tmp/redis.conf
              echo "cluster-announce-port 6379" >> /tmp/redis.conf
              echo "cluster-announce-bus-port 16379" >> /tmp/redis.conf
              exec redis-server /tmp/redis.conf
          ports:
            - name: redis
              containerPort: 6379
            - name: cluster-bus
              containerPort: 16379
          readinessProbe:
            tcpSocket:
              port: 6379
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            tcpSocket:
              port: 6379
            initialDelaySeconds: 15
            periodSeconds: 10
          volumeMounts:
            - name: redis-data
              mountPath: /data
            - name: redis-config
              mountPath: /conf
      volumes:
        - name: redis-data
          hostPath:
            path: /var/lib/redis-cluster/redis-0
            type: Directory
        - name: redis-config
          configMap:
            name: redis-config
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-1
  namespace: redis-lab
spec:
  serviceName: redis-1
  replicas: 1
  selector:
    matchLabels:
      app: redis
      instance: redis-1
  template:
    metadata:
      labels:
        app: redis
        instance: redis-1
    spec:
      nodeName: node2
      tolerations:
        - key: node-role.kubernetes.io/control-plane
          operator: Exists
          effect: NoSchedule
      terminationGracePeriodSeconds: 30
      containers:
        - name: redis
          image: redis:7.2
          imagePullPolicy: IfNotPresent
          env:
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          command:
            - sh
            - -c
            - |
              cp /conf/redis.conf /tmp/redis.conf
              echo "cluster-announce-ip ${POD_IP}" >> /tmp/redis.conf
              echo "cluster-announce-port 6379" >> /tmp/redis.conf
              echo "cluster-announce-bus-port 16379" >> /tmp/redis.conf
              exec redis-server /tmp/redis.conf
          ports:
            - name: redis
              containerPort: 6379
            - name: cluster-bus
              containerPort: 16379
          readinessProbe:
            tcpSocket:
              port: 6379
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            tcpSocket:
              port: 6379
            initialDelaySeconds: 15
            periodSeconds: 10
          volumeMounts:
            - name: redis-data
              mountPath: /data
            - name: redis-config
              mountPath: /conf
      volumes:
        - name: redis-data
          hostPath:
            path: /var/lib/redis-cluster/redis-1
            type: Directory
        - name: redis-config
          configMap:
            name: redis-config
---
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: redis-2
  namespace: redis-lab
spec:
  serviceName: redis-2
  replicas: 1
  selector:
    matchLabels:
      app: redis
      instance: redis-2
  template:
    metadata:
      labels:
        app: redis
        instance: redis-2
    spec:
      nodeName: node3
      tolerations:
        - key: node-role.kubernetes.io/control-plane
          operator: Exists
          effect: NoSchedule
      terminationGracePeriodSeconds: 30
      containers:
        - name: redis
          image: redis:7.2
          imagePullPolicy: IfNotPresent
          env:
            - name: POD_IP
              valueFrom:
                fieldRef:
                  fieldPath: status.podIP
          command:
            - sh
            - -c
            - |
              cp /conf/redis.conf /tmp/redis.conf
              echo "cluster-announce-ip ${POD_IP}" >> /tmp/redis.conf
              echo "cluster-announce-port 6379" >> /tmp/redis.conf
              echo "cluster-announce-bus-port 16379" >> /tmp/redis.conf
              exec redis-server /tmp/redis.conf
          ports:
            - name: redis
              containerPort: 6379
            - name: cluster-bus
              containerPort: 16379
          readinessProbe:
            tcpSocket:
              port: 6379
            initialDelaySeconds: 5
            periodSeconds: 5
          livenessProbe:
            tcpSocket:
              port: 6379
            initialDelaySeconds: 15
            periodSeconds: 10
          volumeMounts:
            - name: redis-data
              mountPath: /data
            - name: redis-config
              mountPath: /conf
      volumes:
        - name: redis-data
          hostPath:
            path: /var/lib/redis-cluster/redis-2
            type: Directory
        - name: redis-config
          configMap:
            name: redis-config
---
apiVersion: batch/v1
kind: Job
metadata:
  name: redis-cluster-init
  namespace: redis-lab
spec:
  backoffLimit: 10
  template:
    spec:
      restartPolicy: OnFailure
      tolerations:
        - key: node-role.kubernetes.io/control-plane
          operator: Exists
          effect: NoSchedule
      containers:
        - name: redis-cluster-init
          image: redis:7.2
          imagePullPolicy: IfNotPresent
          command:
            - sh
            - -c
            - |
              set -e

              REDIS_0="redis-0-0.redis-0.redis-lab.svc.cluster.local"
              REDIS_1="redis-1-0.redis-1.redis-lab.svc.cluster.local"
              REDIS_2="redis-2-0.redis-2.redis-lab.svc.cluster.local"

              for host in "$REDIS_0" "$REDIS_1" "$REDIS_2"; do
                echo "Waiting for $host:6379 ..."
                until redis-cli -h "$host" -p 6379 ping; do
                  sleep 2
                done
              done

              echo "Checking whether cluster is already initialized ..."
              if redis-cli -h "$REDIS_0" -p 6379 cluster info 2>/dev/null | grep -q "cluster_state:ok"; then
                echo "Cluster already initialized."
                exit 0
              fi

              echo "Creating Redis cluster ..."
              yes yes | redis-cli --cluster create \
                ${REDIS_0}:6379 \
                ${REDIS_1}:6379 \
                ${REDIS_2}:6379 \
                --cluster-replicas 0

              echo "Cluster created."
```

- Expected output
```bash
kubectl -n redis-lab exec -it redis-0-0 -- redis-cli -c set hello world
OK
kubectl -n redis-lab exec -it redis-1-0 -- redis-cli -c get hello
"world"
kubectl -n redis-lab exec -it redis-2-0 -- redis-cli -c cluster nodes
1989f045a872423b3b380d4975051e5a5e4dc7ad 10.233.102.175:6379@16379 master - 0 1772787683855 1 connected 0-5460
19d2982eec557ce2eb98cc11ae1fb3ab42d30b5b 10.233.71.17:6379@16379 myself,master - 0 1772787682000 3 connected 10923-16383
4b16ccb23c258e054f6a776a6ab63d18feaf286c 10.233.75.32:6379@16379 master - 0 1772787682850 2 connected 5461-10922
```
