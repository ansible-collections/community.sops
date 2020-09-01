#!/usr/bin/env bash
set -eux

ANSIBLE_ROLES_PATH=.. ansible-playbook setup.yml

if [ "$(which sops)" == "" ]; then
    # sops was not installed
    exit
fi

ANSIBLE_VARS_ENABLED=host_group_vars,community.sops.sops ansible-playbook test-1.yml -v "$@"
