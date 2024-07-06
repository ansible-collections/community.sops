#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -eux

if [ "$(command -v sops)" == "" ]; then
    echo "sops is not installed"
    exit 1
fi

TEST="$1"
if [ "${TEST}" == "" ]; then
    echo "First parameter must be test name!"
    exit 1
fi

shift

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
