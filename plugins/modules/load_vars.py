#!/usr/bin/python
# -*- coding: utf-8 -*-

# Copyright (c) Ansible Project
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
author: Felix Fontein (@felixfontein)
module: load_vars
short_description: Load sops-encrypted variables from files, dynamically within a task
version_added: '0.1.0'
description:
  - Loads sops-encrypted YAML/JSON variables dynamically from a file during task runtime.
  - To assign included variables to a different host than C(inventory_hostname),
    use C(delegate_to) and set C(delegate_facts=true).
options:
  file:
    description:
      - The file name from which variables should be loaded.
      - If the path is relative, it will look for the file in C(vars/) subdirectory of a role or relative to playbook.
    type: path
  name:
    description:
      - The name of a variable into which assign the included vars.
      - If omitted (C(null)) they will be made top level vars.
    type: str
  expressions:
    description:
      - This option controls how Jinja2 expressions in values in the loaded file are handled.
      - If set to C(ignore), expressions will not be evaluated, but treated as regular strings.
      - If set to C(evaluate-on-load), expressions will be evaluated on execution of this module,
        in other words, when the file is loaded.
      - Unfortunately, there is no way for non-core modules to handle expressions "unsafe",
        in other words, evaluate them only on use. This can only achieved by M(ansible.builtin.include_vars),
        which unfortunately cannot handle sops-encrypted files.
    type: str
    default: ignore
    choices:
        - ignore
        - evaluate-on-load
extends_documentation_fragment:
  - community.sops.sops
seealso:
  - module: ansible.builtin.set_fact
  - module: ansible.builtin.include_vars
  - ref: playbooks_delegation
    description: More information related to task delegation.
'''

EXAMPLES = r'''
- name: Include variables of stuff.sops.yaml into the 'stuff' variable
  community.sops.load_vars:
    file: stuff.sops.yaml
    name: stuff
    expressions: evaluate-on-load  # interpret Jinja2 expressions in stuf.sops.yaml on load-time!

- name: Conditionally decide to load in variables into 'plans' when x is 0, otherwise do not
  community.sops.load_vars:
    file: contingency_plan.sops.yaml
    name: plans
    expressions: ignore  # do not interpret possible Jinja2 expressions
  when: x == 0

- name: Load variables into the global namespace
  community.sops.load_vars:
    file: contingency_plan.sops.yaml
'''

RETURN = r'''
ansible_facts:
  description: Variables that were included and their values.
  returned: success
  type: dict
  sample: {'variable': 'value'}
ansible_included_var_files:
  description: A list of files that were successfully included
  returned: success
  type: list
  elements: str
  sample: [ /path/to/file.sops.yaml ]
'''
