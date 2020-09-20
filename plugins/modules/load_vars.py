#!/usr/bin/python
# -*- coding: utf-8 -*-

# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type


DOCUMENTATION = r'''
---
author: Felix Fontein (@felixfontein)
module: load_vars
short_description: Load sops-encrypted variables from files, dynamically within a task
description:
  - Loads sops-encrypted YAML/JSON variables dynamically from a file during task runtime.
  - To assign included variables to a different host than C(inventory_hostname),
    use C(delegate_to) and set C(delegate_facts=yes).
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
  static:
    description:
      - If set to C(false), the contents of the file will be loaded as real variables. This means that Jinja2 expressions
        will be interpreted on usage of the variables.
      - If set to the default value C(true), all strings will be interpreted as strings and will not be templated,
        neither during loading nor during usage.
      - Please note that C(false) is not officially supported by Ansible and is achieved by hacks. We try to make sure
        that it works for all supported versions of Ansible.
      - "NOTE: If set to C(false), DO NOT register the result of the task! This breaks the functionality somehow.
         (Same happens for M(ansible.builtin.include_vars).)"
    type: bool
    default: true
seealso:
- module: ansible.builtin.set_fact
- module: ansible.builtin.include_vars
- ref: playbooks_delegation
  description: More information related to task delegation.
'''

EXAMPLES = r'''
- name: Include variables of stuff.sops.yaml into the 'stuff' variable.
  community.sops.load_vars:
    file: stuff.sops.yaml
    name: stuff
    static: false  # interpret Jinja2 expressions in stuf.sops.yaml on usage of the vars!

- name: Conditionally decide to load in variables into 'plans' when x is 0, otherwise do not.
  community.sops.load_vars:
    file: contingency_plan.sops.yaml
    name: plans
    static: true  # do not interpret possible Jinja2 expressions
  when: x == 0

- name: Load variables into the global namespace
  community.sops.load_vars:
    file: contingency_plan.sops.yaml
'''

RETURN = r'''
ansible_facts:
  description: Variables that were included and their values
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
