#!/bin/sh
set -e
ANSIBLE_VARS_SOPS_PLUGIN_STAGE=task \
ANSIBLE_VARS_SOPS_PLUGIN_CACHE=true \
ansible-playbook playbook.yml -v "$@"
