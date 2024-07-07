#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -eux

if [ "$(command -v sops)" == "" ]; then
    echo "sops is not installed"
    exit 1
fi

if [ $# -lt 2 ]; then
    echo "First parameter must be test name, second parameter the SOPS version!"
    exit 1
fi
TEST="$1"
SOPS_VERSION="$2"

if [ -e "${TEST}/min-version" ]; then
    MIN_VERSION="$(cat "${TEST}/min-version")"
    if [ "$(echo -e "${SOPS_VERSION}\n${MIN_VERSION}" | sort -V | head -1)" != "${MIN_VERSION}" ]; then
        exit
    fi
fi
if [ -e "${TEST}/max-version" ]; then
    MAX_VERSION="$(cat "${TEST}/max-version")"
    if [ "$(echo -e "${SOPS_VERSION}\n${MAX_VERSION}" | sort -V | head -1)" != "${SOPS_VERSION}" ]; then
        exit
    fi
fi

shift 2

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
