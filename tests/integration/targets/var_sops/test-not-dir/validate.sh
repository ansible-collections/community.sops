#!/bin/sh
set -eux

if [ "$1" != 0 ]; then
    exit 1
fi

grep -F "[WARNING]: Found group_vars that is not a directory, skipping:" "$2"
