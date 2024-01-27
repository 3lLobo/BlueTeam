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