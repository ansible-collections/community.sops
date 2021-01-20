# -*- coding: utf-8 -*-
#
#  Copyright 2018 Edoardo Tenani <e.tenani@arduino.cc> [@endorama]
#
# This file is part of Ansible.
#
# Ansible is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Ansible is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Ansible.  If not, see <http://www.gnu.org/licenses/>.
#

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

DOCUMENTATION = """
    name: sops
    author: Edoardo Tenani (@endorama) <e.tenani@arduino.cc>
    short_description: Read sops encrypted file contents
    version_added: '0.1.0'
    description:
        - This lookup returns the contents from a file on the Ansible controller's file system.
        - This lookup requires the C(sops) executable to be available in the controller PATH.
    options:
        _terms:
            description: Path(s) of files to read.
            required: true
        rstrip:
            description: Whether to remove trailing newlines and spaces.
            type: bool
            default: true
        base64:
            description:
                - Base64-encodes the parsed result.
                - Use this if you want to store binary data in Ansible variables.
            type: bool
            default: false
        input_type:
            description:
                - Tell sops how to interpret the encrypted file.
                - By default, sops will chose the input type from the file extension.
                  If it detects the wrong type for a file, this could result in decryption
                  failing.
            type: str
            choices:
                - binary
                - json
                - yaml
                - dotenv
        output_type:
            description:
                - Tell sops how to interpret the decrypted file.
                - By default, sops will chose the output type from the file extension.
                  If it detects the wrong type for a file, this could result in decryption
                  failing.
            type: str
            choices:
                - binary
                - json
                - yaml
                - dotenv
        empty_on_not_exist:
            description:
                - When set to C(true), will not raise an error when a file cannot be found,
                  but return an empty string instead.
            type: bool
            default: false
    extends_documentation_fragment:
        - community.sops.sops
        - community.sops.sops.ansible_variables
    notes:
        - This lookup does not understand 'globbing' - use the fileglob lookup instead.
"""

EXAMPLES = """
tasks:
  - name: Output secrets to screen (BAD IDEA!)
    ansible.builtin.debug:
        msg: "Content: {{ lookup('community.sops.sops', item) }}"
    loop:
        - sops-encrypted-file.enc.yaml

  - name: Add SSH private key
    ansible.builtin.copy:
        content: "{{ lookup('community.sops.sops', user + '-id_rsa') }}"
        dest: /home/{{ user }}/.ssh/id_rsa
        owner: "{{ user }}"
        group: "{{ user }}"
        mode: 0600
    no_log: true  # avoid content to be written to log

  - name: The file file.json is a YAML file, which contains the encryption of binary data
    ansible.builtin.debug:
        msg: "Content: {{ lookup('community.sops.sops', 'file.json', input_type='yaml', output_type='binary') }}"

"""

RETURN = """
    _raw:
        description: Decrypted file content.
        type: list
        elements: str
"""

import base64

from ansible.errors import AnsibleLookupError
from ansible.plugins.lookup import LookupBase
from ansible.module_utils._text import to_native
from ansible_collections.community.sops.plugins.module_utils.sops import Sops, SopsError

from ansible.utils.display import Display
display = Display()


class LookupModule(LookupBase):

    def run(self, terms, variables=None, **kwargs):
        self.set_options(var_options=variables, direct=kwargs)
        rstrip = self.get_option('rstrip')
        use_base64 = self.get_option('base64')
        input_type = self.get_option('input_type')
        output_type = self.get_option('output_type')
        empty_on_not_exist = self.get_option('empty_on_not_exist')

        ret = []

        def get_option_value(argument_name):
            return self.get_option(argument_name)

        for term in terms:
            display.debug("Sops lookup term: %s" % term)
            lookupfile = self.find_file_in_search_path(variables, 'files', term, ignore_missing=empty_on_not_exist)
            display.vvvv(u"Sops lookup using %s as file" % lookupfile)

            if not lookupfile:
                if empty_on_not_exist:
                    ret.append('')
                    continue
                raise AnsibleLookupError("could not locate file in lookup: %s" % to_native(term))

            try:
                output = Sops.decrypt(
                    lookupfile, display=display, rstrip=rstrip, decode_output=not use_base64,
                    input_type=input_type, output_type=output_type, get_option_value=get_option_value)
            except SopsError as e:
                raise AnsibleLookupError(to_native(e))

            if use_base64:
                output = to_native(base64.b64encode(output))

            ret.append(output)

        return ret
