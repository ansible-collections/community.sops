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

for TEST in $(find . -maxdepth 1 -type d -name 'test-*' | sort); do
    (
        cd "${TEST}"
        if [ -x "setup.sh" ]; then
            ./setup.sh
        fi
        if [ -x "run.sh" ]; then
            ANSIBLE_VARS_ENABLED=host_group_vars,community.sops.sops ./run.sh "$@" 2>&1 | tee out
            RESULT=${PIPESTATUS[0]}
        else
            ANSIBLE_VARS_ENABLED=host_group_vars,community.sops.sops ansible-playbook playbook.yml -i hosts -v "$@" 2>&1 | tee out
            RESULT=${PIPESTATUS[0]}
        fi
        ./validate.sh "${RESULT}" out
    )
done
