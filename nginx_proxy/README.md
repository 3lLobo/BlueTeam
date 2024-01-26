# Proxy Nginx

Route traffic into minikube through a nginx proxy.

## Config

Populate the `.env` file.
Generate the `nginx.conf` from the template `nginx.conf.example`:
  
```bash
make

```

## Up nginx

Good old:
```bash
docker-compose up
```