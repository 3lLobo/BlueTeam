# Copyright (c) Tailscale Inc & AUTHORS
# SPDX-License-Identifier: BSD-3-Clause


TS_ROUTES ?= ""
SA_NAME ?= tailscale
ROLE_NAME ?= tailscale
TS_KUBE_SECRET ?= tailscale

rbac:
	@sed -e "s;{{TS_KUBE_SECRET}};$(TS_KUBE_SECRET);g" role.yaml | sed -e "s;{{ROLE_NAME}};$(ROLE_NAME);g"
	@echo "---"
	@sed -e "s;{{SA_NAME}};$(SA_NAME);g" rolebinding.yaml | sed -e "s;{{ROLE_NAME}};$(ROLE_NAME);g"
	@echo "---"
	@sed -e "s;{{SA_NAME}};$(SA_NAME);g" sa.yaml


authkey:
	@sed -e "s;{{TS_KUBE_SECRET}};$(TS_KUBE_SECRET);g" authkey.yaml | sed -e "s;{{XXX}};$(XXX);g"

sidecar:
	@sed -e "s;{{TS_KUBE_SECRET}};$(TS_KUBE_SECRET);g" sidecar.yaml | sed -e "s;{{SA_NAME}};$(SA_NAME);g"

userspace-sidecar:
	@sed -e "s;{{TS_KUBE_SECRET}};$(TS_KUBE_SECRET);g" userspace-sidecar.yaml | sed -e "s;{{SA_NAME}};$(SA_NAME);g"

proxy:
	@sed -e "s;{{TS_KUBE_SECRET}};$(TS_KUBE_SECRET);g" proxy.yaml | sed -e "s;{{SA_NAME}};$(SA_NAME);g" | sed -e "s;{{TS_AUTHKEY}};$(TS_AUTHKEY);g" | sed -e "s;{{CONTAINER_NAME}};$(CONTAINER_NAME);g" | sed -e "s;{{TS_DEST_IP}};$(TS_DEST_IP);g"

subnet-router:
	@sed -e "s;{{TS_KUBE_SECRET}};$(TS_KUBE_SECRET);g" subnet.yaml | sed -e "s;{{SA_NAME}};$(SA_NAME);g" | sed -e "s;{{TS_ROUTES}};$(TS_ROUTES);g"
