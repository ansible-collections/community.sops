#!/bin/sh
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -e
ANSIBLE_VARS_SOPS_PLUGIN_VALID_EXTENSIONS=".yml, .yaml, .json" \
ansible-playbook playbook.yml -i hosts -v "$@"
