#!/bin/sh
# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

if [ "$1" != "--keyservice" ] || [ "$2" != "a" ] || [ "$3" != "--keyservice" ] || [ "$4" != "b" ] || [ "$5" != "--input-type" ] || [ "$6" != "yaml" ] || [ "$7" != "--output-type" ] || [ "$8" != "yaml" ] || [ "$9" != "--decrypt" ] || [ "${10}" != "/dev/stdin" ] || [ "${11}" != "" ]; then
    echo "Command (fake-sops-rep): $*" > /dev/stderr
    exit 1
fi
if [ "${AWS_SESSION_TOKEN}" != "zzz" ]; then
    echo "AWS_SESSION_TOKEN is '${AWS_SESSION_TOKEN}'" > /dev/stderr
    exit 1
fi
echo 'fake sops output 3'
