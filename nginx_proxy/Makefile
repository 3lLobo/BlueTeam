SHELL := /bin/bash

default: nginx_config

# Populate the nginx template with the environment variables
nginx_config:
	@echo "Generating default.config..."
	@source .env && envsubst < default.conf.example | sed 's/nvar_/$$/g' > nginx/default.conf
	@echo "Done!"

