# Wolf SOC on k8

<!-- ## Elastic with Traefic ingress

Install Traefik stuff:
```bash
# Install Traefik Resource Definitions:
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v2.10/docs/content/reference/dynamic-configuration/kubernetes-crd-definition-v1.yml

# Install RBAC for Traefik:
kubectl apply -f https://raw.githubusercontent.com/traefik/traefik/v2.10/docs/content/reference/dynamic-configuration/kubernetes-crd-rbac.yml
```
Now cert-manager:
```bash
kubectl apply -f https://github.com/cert-manager/cert-manager/releases/download/v1.13.3/cert-manager.yaml
```



Download the example from [here](https://download-directory.github.io/?url=https%3A%2F%2Fgithub.com%2Felastic%2Fcloud-on-k8s%2Ftree%2Fmain%2Fconfig%2Frecipes%2Ftraefik). -->


## Elastic

Following [these](https://www.elastic.co/guide/en/cloud-on-k8s/current/k8s-deploy-eck.html) docs, first apply `crds` and `operator`:
```
kubectl create -f https://download.elastic.co/downloads/eck/2.11.0/crds.yaml 
kubectl apply -f https://download.elastic.co/downloads/eck/2.11.0/operator.yaml

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

### NodePorts

Apply the `nodeport-svc.yaml` and let Minikube bind the ports to the host:
```bash
minikube service --all --url
```

### IP tables

TODO: Route the incoming traffic to the minikube ip.



### Tailscale tunnel

We tunnel each service through tailscale.

For each service we deploy a proxy as described in the [tailscale docs](https://tailscale.com/kb/1185/kubernetes/).

First create the `.env` with the necessary api keys.
Then run the `deploy_proxies.py` script:
```
python3 deploy_proxies.py
```

Check the `log.txt` file for incommodities.
Then run:
```
kubectl get pods
```
to check that all pods are running correctly.

### MiniKube ingress

Install the ingress pluggins first:
```bash
minikube addons enable ingress
minikube addons enable ingress-dns
```
Then [set up dnsq](https://minikube.sigs.k8s.io/docs/handbook/addons/ingress-dns/) on your machine.

Now apply the ingress file.


## PiHole 🍓

Set up PiHole on K8 and use it as tailscale DNS server.
This way we can resolve all services by name.
Further gooddies are the ad blocking and DNS statistics.
We follow [this random dudes blocq](https://greg.jeanmart.me/2020/04/13/self-host-pi-hole-on-kubernetes-and-block-ad/).

### Steps
> U need Helm!

1. Create a `pihole` namespace.
2. Create persistent volumes.
3. Create the pv claim.
4. Install PiHole with helm.

```
kubectl create namespace pihole
kubectl apply -f pihole/pihole.persistentvolume.yaml
kubectl apply -f pihole/pihole.persistentvolumeclaim.yaml

helm repo add mojo2600 https://mojo2600.github.io/pihole-kubernetes/
helm repo update
helm install k8 mojo2600/pihole -n pihole
```

### TailScale proxy

Similar game to the elastic proxy.
We need to deploy a proxy for each piholes service.

```bash
python3 deploy_proxies.py k8-pihole-dhcp k8-pihole-dns-tcp k8-pihole-dns-udp k8-pihole-web -n pihole
```
Then check the logs of the new tailscale proxy pods and authenticate via the URL.
