source .env && envsubst < nginx/nginx.conf.example | sed 's/nvar_/$/g' > nginx/nginx.conf
