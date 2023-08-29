# Wolf SOC on k8

## Elastic

Following [these](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-eck.html) docs, first apply `crds` and `operator`:
```
kubectl create -f https://download.elastic.co/downloads/eck/2.9.0/crds.yaml 
kubectl apply -f https://download.elastic.co/downloads/eck/2.9.0/operator.yaml

```

Check the operator logs with:
```
kubectl -n elastic-system logs -f statefulset.apps/elastic-operator
```

Deploy the stack:
```
kubectl apply -f https://raw.githubusercontent.com/elastic/cloud-on-k8s/main/config/recipes/elastic-agent/fleet-kubernetes-integration.yaml
```

Get the elastic pwd with:
```
PASSWORD=$(kubectl get secret elasticsearch-es-elastic-user -o go-template='{{.data.elastic | base64decode}}')
```

## Tailscale tunnel

We tunnel each service through tailscale

