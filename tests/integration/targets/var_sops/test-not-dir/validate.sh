#!/bin/sh
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -eux

if [ "$1" != 0 ]; then
    exit 1
fi

grep -F "[WARNING]: Found group_vars that is not a directory, skipping:" "$2"
