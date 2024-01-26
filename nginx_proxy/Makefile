SHELL := /bin/bash

default: nginx_config

# Populate the nginx template with the environment variables
nginx_config:
	@echo "Generating nginx.config..."
	@source .env && envsubst < nginx.conf.example | sed 's/nvar_/$$/g' > nginx/nginx.conf
	@echo "Done!"

