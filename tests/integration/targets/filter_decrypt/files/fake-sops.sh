#!/bin/sh
if [ "$1" != "--enable-local-keyservice" ] || [ "$2" != "--input-type" ] || [ "$3" != "yaml" ] || [ "$4" != "--output-type" ] || [ "$5" != "yaml" ] || [ "$6" != "--decrypt" ] || [ "$7" != "/dev/stdin" ] || [ "$8" != "" ]; then
    echo "Command (fake-sops): $*" > /dev/stderr
    exit 1
fi
if [ "${AWS_ACCESS_KEY_ID}" != "xxx" ]; then
    echo "AWS_ACCESS_KEY_ID is '${AWS_ACCESS_KEY_ID}'" > /dev/stderr
    exit 1
fi
echo 'fake sops output'
