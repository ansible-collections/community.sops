#!/bin/sh
if [ "$1" != "--enable-local-keyservice" ] || [ "$2" != "--decrypt" ] || [ "$(basename "$3")" != "simple.sops.yaml" ] || [ "$4" != "" ]; then
    echo "Command (fake-sops): $*" > /dev/stderr
    exit 1
fi
if [ "${AWS_ACCESS_KEY_ID}" != "xxx" ]; then
    echo "AWS_ACCESS_KEY_ID is '${AWS_ACCESS_KEY_ID}'" > /dev/stderr
    exit 1
fi
echo 'fake sops output'
