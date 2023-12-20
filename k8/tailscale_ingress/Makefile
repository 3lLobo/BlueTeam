# Copyright (c) Tailscale Inc & AUTHORS
# SPDX-License-Identifier: BSD-3-Clause

SHELL := /bin/bash

include .env

CLIENT_ID ?= ""
CLIENT_SECRET ?= ""


operator:
	@sed -e "s;{{ CLIENT_ID }};$(CLIENT_ID);g" operator.yaml | sed -e "s;{{ CLIENT_SECRET }};$(CLIENT_SECRET);g"
