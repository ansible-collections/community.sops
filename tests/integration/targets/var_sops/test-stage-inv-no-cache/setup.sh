#!/bin/sh
rm -rf group_vars/
mkdir -p group_vars/
cp 1.sops.yml group_vars/all.sops.yaml
