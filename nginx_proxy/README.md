# Proxy Nginx

Route traffic into minikube through a nginx proxy.

## Certs 

[Generate local certs](https://gist.github.com/cecilemuller/9492b848eb8fe46d462abeb26656c4f8)

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