SHELL := /bin/bash

default: ssl_config

# Populate the nginx template with the environment variables
ssl_config:
	@echo "Generating nginx.config for ssl..."
	@source .env && envsubst < ssl.conf.example | sed 's/nvar_/$$/g' > nginx/nginx.conf
	@echo "Done!"

stream_config:
	@echo "Generating nginx.config for stream..."
	@source .env && envsubst < stream.conf.example | sed 's/nvar_/$$/g' > nginx/nginx.conf
	@echo "Done!"

cert_gen:
	@source .env && echo "Generating self-signed certificate for ${SERVER_NAME}..."
	@source .env && cd nginx/ssl && openssl req -new -nodes -newkey rsa:2048 -keyout "${SERVER_NAME}.key" -out "${SERVER_NAME}.csr" -subj "/C=US/ST=YourState/L=YourCity/O=Example-Certificates/CN=${SERVER_NAME}" && openssl x509 -req -sha256 -days 1024 -in "${SERVER_NAME}.csr" -CA RootCA.pem -CAkey RootCA.key -CAcreateserial -extfile domains.ext -out "${SERVER_NAME}.crt"
	@echo "Done!"