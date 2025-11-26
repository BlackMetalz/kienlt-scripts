#!/bin/bash
# k8s-user-manager.sh

set -e
# Namespace to work with
NAMESPACE="working-namespace" 

function list_roles() {
    echo "==> Available roles in namespace ${NAMESPACE}:"
    kubectl get role -n ${NAMESPACE} --no-headers | awk '{print "  - " $1}'
}

function create_user() {
    local USERNAME=$1
    local ROLE_NAME=$2

    # Nếu không truyền role, list và cho chọn (tất nhiên là role của namepspace hiện tại nhé xD)
    if [ -z "$ROLE_NAME" ]; then
        echo "==> Available roles:"
        kubectl get role -n ${NAMESPACE} --no-headers | awk '{print NR". " $1}'
        echo -n "Choose role number: "
        read ROLE_NUM
        ROLE_NAME=$(kubectl get role -n ${NAMESPACE} --no-headers | awk "NR==${ROLE_NUM} {print \$1}")

        if [ -z "$ROLE_NAME" ]; then
            echo "Invalid selection!"
            exit 1
        fi
    fi

    echo "==> Creating user: ${USERNAME} with role: ${ROLE_NAME}"

    # Check role exists
    if ! kubectl get role ${ROLE_NAME} -n ${NAMESPACE} &>/dev/null; then
        echo "Error: Role ${ROLE_NAME} does not exist in namespace ${NAMESPACE}"
        exit 1
    fi

    # 1. Generate key
    echo "  [1/7] Generating private key..."
    openssl genrsa -out ${USERNAME}.key 2048 2>/dev/null

    # 2. Create CSR
    echo "  [2/7] Creating certificate signing request..."
    openssl req -new -key ${USERNAME}.key -out ${USERNAME}.csr \
        -subj "/CN=${USERNAME}/O=developers" 2>/dev/null

    # 3. Submit CSR to K8s
    echo "  [3/7] Submitting CSR to Kubernetes..."
    cat <<EOF | kubectl apply -f - >/dev/null
apiVersion: certificates.k8s.io/v1
kind: CertificateSigningRequest
metadata:
  name: ${USERNAME}
spec:
  request: $(cat ${USERNAME}.csr | base64 | tr -d '\n')
  signerName: kubernetes.io/kube-apiserver-client
  usages:
  - client auth
EOF

    # 4. Approve CSR
    echo "  [4/7] Approving certificate..."
    kubectl certificate approve ${USERNAME} >/dev/null
    sleep 2

    # 5. Get certificate
    echo "  [5/7] Retrieving signed certificate..."
    kubectl get csr ${USERNAME} -o jsonpath='{.status.certificate}' | base64 -d > ${USERNAME}.crt

    # 6. Create RoleBinding
    echo "  [6/7] Creating role binding..."
    kubectl create rolebinding ${USERNAME}-${ROLE_NAME}-binding \
      --role=${ROLE_NAME} \
      --user=${USERNAME} \
      --namespace=${NAMESPACE} 2>/dev/null || echo "    (RoleBinding already exists)"

    # 7. Generate kubeconfig
    echo "  [7/7] Generating kubeconfig..."
    CLUSTER=$(kubectl config view -o jsonpath='{.clusters[0].name}')

    kubectl config set-credentials ${USERNAME} \
      --client-certificate=${USERNAME}.crt \
      --client-key=${USERNAME}.key \
      --embed-certs=true >/dev/null

    kubectl config set-context ${USERNAME}-context \
      --cluster=${CLUSTER} \
      --user=${USERNAME} \
      --namespace=${NAMESPACE} >/dev/null

    kubectl config view --flatten \
      --context=${USERNAME}-context \
      --minify > ${USERNAME}-kubeconfig

    # Cleanup temp context
    kubectl config delete-context ${USERNAME}-context >/dev/null 2>&1
    kubectl config unset users.${USERNAME} >/dev/null 2>&1

    echo ""
    echo "==> ✅ User created successfully!"
    echo "    Username: ${USERNAME}"
    echo "    Role: ${ROLE_NAME}"
    echo "    Namespace: ${NAMESPACE}"
    echo "    Kubeconfig: ${USERNAME}-kubeconfig"
    echo ""
    echo "Send '${USERNAME}-kubeconfig' to the user"
}

function delete_user() {
    local USERNAME=$1

    echo "==> Deleting user: ${USERNAME}"

    # Delete all rolebindings for this user
    BINDINGS=$(kubectl get rolebindings -n ${NAMESPACE} -o json | \
        jq -r ".items[] | select(.subjects[]?.name==\"${USERNAME}\") | .metadata.name")

    if [ ! -z "$BINDINGS" ]; then
        echo "$BINDINGS" | while read binding; do
            echo "  Deleting rolebinding: $binding"
            kubectl delete rolebinding $binding -n ${NAMESPACE}
        done
    fi

    # Delete CSR
    kubectl delete csr ${USERNAME} 2>/dev/null || true

    # Delete local files
    rm -f ${USERNAME}.key ${USERNAME}.csr ${USERNAME}.crt ${USERNAME}-kubeconfig

    echo "==> ✅ User deleted!"
}

function list_users() {
    echo "==> Users in namespace ${NAMESPACE}:"
    echo ""
    printf "%-20s %-30s\n" "USERNAME" "ROLE"
    printf "%-20s %-30s\n" "--------" "----"
    kubectl get rolebindings -n ${NAMESPACE} -o json | \
        jq -r '.items[] | select(.subjects[]?.kind=="User") |
        "\(.subjects[].name) \(.roleRef.name)"' | \
        while read user role; do
            printf "%-20s %-30s\n" "$user" "$role"
        done
}

function show_user_permissions() {
    local USERNAME=$1

    if [ -z "$USERNAME" ]; then
        echo "Usage: $0 permissions <username>"
        exit 1
    fi

    echo "==> Permissions for user: ${USERNAME} in namespace ${NAMESPACE}"
    kubectl auth can-i --list --as=${USERNAME} -n ${NAMESPACE}
}

# Main
case "$1" in
    create)
        if [ -z "$2" ]; then
            echo "Usage: $0 create <username> [role-name]"
            echo ""
            list_roles
            exit 1
        fi
        create_user $2 $3
        ;;
    delete)
        if [ -z "$2" ]; then
            echo "Usage: $0 delete <username>"
            exit 1
        fi
        delete_user $2
        ;;
    list)
        list_users
        ;;
    roles)
        list_roles
        ;;
    permissions)
        show_user_permissions $2
        ;;
    *)
        echo "Kubernetes User Manager for namespace: ${NAMESPACE}"
        echo ""
        echo "Usage: $0 {create|delete|list|roles|permissions}"
        echo ""
        echo "Commands:"
        echo "  roles                      - List available roles"
        echo "  create <user> [role]       - Create user (interactive role selection if not specified)"
        echo "  delete <user>              - Delete user and cleanup"
        echo "  list                       - List all users and their roles"
        echo "  permissions <user>         - Show user permissions"
        echo ""
        echo "Examples:"
        echo "  $0 roles"
        echo "  $0 create kienlt-dev                    # Interactive role selection"
        echo "  $0 create kienlt-dev kienlt-admin         # Direct role assignment"
        echo "  $0 list"
        echo "  $0 permissions kienlt-dev"
        echo "  $0 delete kienlt-dev"
        exit 1
        ;;
esac
