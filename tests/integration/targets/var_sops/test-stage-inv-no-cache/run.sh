#!/bin/sh
set -e
ANSIBLE_VARS_SOPS_PLUGIN_STAGE=inventory \
ANSIBLE_VARS_SOPS_PLUGIN_CACHE=false \
ansible-playbook playbook.yml -i hosts -v "$@"
