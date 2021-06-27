# -*- coding: utf-8 -*-

# Copyright: (c) 2021, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import absolute_import, division, print_function
__metaclass__ = type

from ansible.errors import AnsibleError, AnsibleFilterError
from ansible.module_utils.common.text.converters import to_bytes, to_native
from ansible.utils.display import Display

from ansible_collections.community.sops.plugins.module_utils.sops import Sops, SopsError


_VALID_TYPES = set(['binary', 'json', 'yaml', 'dotenv'])


def decrypt_filter(data, input_type='yaml', output_type='yaml', sops_binary='sops', rstrip=True, decode_output=True,
                   aws_profile=None, aws_access_key_id=None, aws_secret_access_key=None, aws_session_token=None,
                   config_path=None, enable_local_keyservice=None, keyservice=None):
    '''Decrypt sops-encrypted data.'''

    # Check parameters
    if input_type not in _VALID_TYPES:
        raise AnsibleFilterError('input_type must be one of {expected}; got "{value}"'.format(
            expected=', '.join(sorted(_VALID_TYPES)), value=input_type))
    if output_type not in _VALID_TYPES:
        raise AnsibleFilterError('output_type must be one of {expected}; got "{value}"'.format(
            expected=', '.join(sorted(_VALID_TYPES)), value=output_type))

    # Create option value querier
    def get_option_value(argument_name):
        if argument_name == 'sops_binary':
            return sops_binary
        if argument_name == 'aws_profile':
            return aws_profile
        if argument_name == 'aws_access_key_id':
            return aws_access_key_id
        if argument_name == 'aws_secret_access_key':
            return aws_secret_access_key
        if argument_name == 'aws_session_token':
            return aws_session_token
        if argument_name == 'config_path':
            return config_path
        if argument_name == 'enable_local_keyservice':
            return enable_local_keyservice
        if argument_name == 'keyservice':
            return keyservice
        raise AssertionError('internal error: should not be reached')

    # Decode
    data = to_bytes(data)
    try:
        output = Sops.decrypt(
            None, content=data, display=Display(), rstrip=rstrip, decode_output=decode_output,
            input_type=input_type, output_type=output_type, get_option_value=get_option_value)
    except SopsError as e:
        raise AnsibleFilterError(to_native(e))

    return output


class FilterModule(object):
    '''Ansible jinja2 filters'''

    def filters(self):
        return {
            'decrypt': decrypt_filter,
        }
