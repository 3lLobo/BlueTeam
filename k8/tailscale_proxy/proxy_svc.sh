# kibana
export CONTAINER_NAME="tailsace-kibana-pod"
export SA_NAME="tailscale-kibana"
export TS_KUBE_SECRET="tailscale-kibana-secret"

make rbac | kubectl apply -f-

export TS_DEST_IP="$(kubectl get svc kibana-kb-http -o=jsonpath='{.spec.clusterIP}')"

make proxy | kubectl apply -f-