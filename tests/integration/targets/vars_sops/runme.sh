#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -eux

# Install sops
ANSIBLE_ROLES_PATH=.. ansible-playbook setup.yml

if [ "$(command -v sops)" == "" ]; then
    # sops was not installed
    exit
fi

./run-tests.sh
