#!/bin/sh
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

set -eux

if [ "$1" != 4 ]; then
    exit 1
fi

( grep -F "ERROR! error with file" "$2" && grep "sops metadata not found" "$2" ) || ( grep -F "[ERROR]: error with file" "$2" && grep "sops metadata not found" "$2" ) || ( grep -F "ERROR! SOPS vars plugin: file" "$2" && grep "is not encrypted" "$2" ) || ( grep -F "[ERROR]: SOPS vars plugin: file" "$2" && grep "is not encrypted" "$2" )
( grep -vF "[WARNING]: SOPS vars plugin: skipping unencrypted file" "$2" )
