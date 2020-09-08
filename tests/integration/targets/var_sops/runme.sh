#!/usr/bin/env bash
set -eux

# Don't run this on Ansible 2.9
if (ansible --version | grep '^ansible 2\.9\.'); then
    # Ansible 2.9 doesn't know about var plugins
    exit
fi

# Install sops
ANSIBLE_ROLES_PATH=.. ansible-playbook setup.yml

if [ "$(which sops)" == "" ]; then
    # sops was not installed
    exit
fi

# First test
ANSIBLE_VARS_ENABLED=host_group_vars,community.sops.sops ansible-playbook test-1.yml -v "$@"
