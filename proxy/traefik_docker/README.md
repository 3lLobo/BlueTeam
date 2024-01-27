# Route incoming traffic to K8

Incoming traffic on the node are routed to the Minikube cluster.

## Docker traefik

Set the `minikube ip` in `/etc/hosts` to `minikube.local`. Then run start the docker-compose file.

```bash
docker-compose up
```
