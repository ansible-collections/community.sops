#!/usr/bin/env bash

set -eux

ANSIBLE_CONFIG=ansible.cfg ansible-playbook -v playbook.yml
