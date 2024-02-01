# Proxy Nginx

Route traffic into minikube through a nginx proxy.

## Certs 

For the SSL option [Generate local certs](https://gist.github.com/cecilemuller/9492b848eb8fe46d462abeb26656c4f8).
Place the files in the `nginx/ssl` folder.

## Config

Populate the `.env` file.
Set a static IP for the nginx container, different from `minikube ip`.
Generate the `nginx.conf` from the one of the templates.
  
```bash
make
```

### SSL

This config sets up a SSL proxy for all the given ports.
The SSL certs shown to the client are the ones generated in the `nginx/ssl` folder.

### Stream

Streams all traffic to the upstream server:port.
Should work for all sort of TCP traffic. Not sure about UDP.
Certificates shown to the client are the upstream ones.

## Up nginx

Good old:
```bash
docker-compose up
```

Read the logs:
```bash
docker exec nginx  tail -f /var/log/nginx/nginx-access.log
```

