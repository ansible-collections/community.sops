#!/bin/sh
set -eux

if [ $1 != 4 ]; then
    exit 1
fi

cat $2
grep -F "ERROR! error with file" $2
grep "sops metadata not found" $2
