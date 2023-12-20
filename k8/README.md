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

## Tailscale operator

Apply a k8 operator which enables ingress routes to expose services on the tailscale network.
Follow [this tutorial](https://tailscale.com/kb/1215/oauth-clients#setting-up-an-oauth-client).

1. Craete an OAuth id on the admin console.
2. Store the id and secret in the `.env`.
3. Deploy the operator
```bash
cd tailscale
make operator | kubectl apply -f-
```
4. Deploy an Ingress-controler
```bash
kubectl apply -f https://raw.githubusercontent.com/kubernetes/ingress-nginx/controller-v1.8.2/deploy/static/provider/cloud/deploy.yaml
```
5. 


## Tailscale tunnel [depreciated]

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
