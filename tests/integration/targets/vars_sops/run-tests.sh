#!/usr/bin/env bash
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -eux

if [ "$(command -v sops)" == "" ]; then
    echo "sops is not installed"
    exit 1
fi

# Get hold of SOPS version
set +e
SOPS_VERSION_RAW="$(sops --version --disable-version-check)" || SOPS_VERSION_RAW="$(sops --version)"
set -e
SOPS_VERSION="$(echo "${SOPS_VERSION_RAW}" | sed -E 's/^sops ([0-9.]+).*/\1/g')"

# Run all tests
for TEST in $(find . -maxdepth 1 -type d -name 'test-*' | sort); do
    ./run-test.sh "${TEST}" "${SOPS_VERSION}" "$@"
done
