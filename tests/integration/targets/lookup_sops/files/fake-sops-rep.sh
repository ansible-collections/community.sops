#!/bin/sh
if [ "$1" != "--keyservice" ] || [ "$2" != "a" ] || [ "$3" != "--keyservice" ] || [ "$4" != "b" ] || [ "$5" != "--decrypt" ] || [ "$(basename "$6")" != "simple.sops.yaml" ] || [ "$7" != "" ]; then
    echo "Command (fake-sops-rep): $*" > /dev/stderr
    exit 1
fi
if [ "${AWS_SESSION_TOKEN}" != "zzz" ]; then
    echo "AWS_SESSION_TOKEN is '${AWS_SESSION_TOKEN}'" > /dev/stderr
    exit 1
fi
echo 'fake sops output 3'
