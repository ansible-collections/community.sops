#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -eux

if [ "$(command -v sops)" == "" ]; then
    echo "sops is not installed"
    exit 1
fi

for TEST in $(find . -maxdepth 1 -type d -name 'test-*' | sort); do
    ./run-test.sh "${TEST}" "$@"
done
