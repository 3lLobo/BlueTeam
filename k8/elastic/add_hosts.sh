# !/bin/bash
# Add k8 domain-names services to /etc/hosts

# Get k8 domain-names
k8_domain_names=$(kubectl get svc --all-namespaces -o jsonpath="{..spec.clusterIP} {..metadata.name}" | awk '{print $1" "$2}')

echo $k8_domain_names
# Get k8 service names
k8_service_names=$(kubectl get svc --all-namespaces -o jsonpath="{..metadata.name}")

echo $k8_service_names

HOST_IP=$(minikube ip)
HOST_IP=$(hostname -I | awk '{print $1}')

# Add k8 domain-names services to /etc/hosts
for k8_domain_name in $k8_service_names
do
    if [[ $k8_domain_name == *"http"* ]]; then
        # doesn't end with 'nodeport'?
        if [[ $k8_domain_name != *"nodeport"* ]]; then
            # append .default.svc to the svc name
            k8_domain_name="$k8_domain_name.default.svc"
            echo $k8_domain_name
            echo "$HOST_IP $k8_domain_name" >> ./hosts
        fi
    fi
done
