#!/bin/sh
if [ "$1" != "--config" ] || [ "$2" != "/path/to/asdf" ] || [ "$3" != "--decrypt" ] || [ "$(basename "$4")" != "simple.sops.yaml" ] || [ "$5" != "" ]; then
    echo "Command (fake-sops-val): $*" > /dev/stderr
    exit 1
fi
if [ "${AWS_SECRET_ACCESS_KEY}" != "yyy" ]; then
    echo "AWS_SECRET_ACCESS_KEY is '${AWS_SECRET_ACCESS_KEY}'" > /dev/stderr
    exit 1
fi
echo 'fake sops output 2'
