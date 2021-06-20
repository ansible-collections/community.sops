#!/bin/sh
if [ "$1" != "--config" ] || [ "$2" != "/path/to/asdf" ] || [ "$3" != "--input-type" ] || [ "$4" != "yaml" ] || [ "$5" != "--output-type" ] || [ "$6" != "yaml" ] || [ "$7" != "--decrypt" ] || [ "$8" != "/dev/stdin" ] || [ "$9" != "" ]; then
    echo "Command (fake-sops-val): $*" > /dev/stderr
    exit 1
fi
if [ "${AWS_SECRET_ACCESS_KEY}" != "yyy" ]; then
    echo "AWS_SECRET_ACCESS_KEY is '${AWS_SECRET_ACCESS_KEY}'" > /dev/stderr
    exit 1
fi
echo 'fake sops output 2'
