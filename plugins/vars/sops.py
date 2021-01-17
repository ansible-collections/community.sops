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

DOCUMENTATION = '''
    name: sops
    author: Edoardo Tenani (@endorama) <e.tenani@arduino.cc>
    short_description: Loading sops-encrypted vars files
    version_added: '0.1.0'
    description:
        - Load encrypted YAML files into corresponding groups/hosts in group_vars/ and host_vars/ directories.
        - Files are encrypted prior to reading, making this plugin an effective companion to host_group_vars plugin.
        - Files are restricted to .sops.yaml, .sops.yml, .sops.json extensions.
        - Hidden files are ignored.
    options:
      _valid_extensions:
        default: [".sops.yml", ".sops.yaml", ".sops.json"]
        description:
          - "Check all of these extensions when looking for 'variable' files which should be YAML or JSON or vaulted versions of these."
          - 'This affects vars_files, include_vars, inventory and vars plugins among others.'
        type: list
      stage:
        version_added: 0.2.0
        ini:
          - key: vars_stage
            section: community.sops
        env:
          - name: ANSIBLE_VARS_SOPS_PLUGIN_STAGE
      cache:
        description:
          - Whether to cache decrypted files or not.
          - If the cache is disabled, the files will be decrypted for almost every task. This is very slow!
          - Only disable caching if you modify the variable files during a playbook run and want the updated
            result to be available from the next task on.
          - "Note that setting I(stage) to C(inventory) has the same effect as setting I(cache) to C(true):
             the variables will be loaded only once (during inventory loading) and the vars plugin will not
             be called for every task."
        type: bool
        default: true
        version_added: 0.2.0
        ini:
          - key: vars_cache
            section: community.sops
        env:
          - name: ANSIBLE_VARS_SOPS_PLUGIN_CACHE
    extends_documentation_fragment:
        - ansible.builtin.vars_plugin_staging
        - community.sops.sops
'''

import os
from ansible.errors import AnsibleParserError
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.plugins.vars import BaseVarsPlugin
from ansible.inventory.host import Host
from ansible.inventory.group import Group
from ansible.utils.vars import combine_vars
from ansible_collections.community.sops.plugins.module_utils.sops import Sops, SopsError

from ansible.utils.display import Display
display = Display()


FOUND = {}
DECRYPTED = {}
DEFAULT_VALID_EXTENSIONS = [".sops.yaml", ".sops.yml", ".sops.json"]


class VarsModule(BaseVarsPlugin):

    def get_vars(self, loader, path, entities, cache=None):
        ''' parses the inventory file '''

        if not isinstance(entities, list):
            entities = [entities]

        super(VarsModule, self).get_vars(loader, path, entities)

        def get_option_value(argument_name):
            return self.get_option(argument_name)

        if cache is None:
            cache = self.get_option('cache')

        data = {}
        for entity in entities:
            if isinstance(entity, Host):
                subdir = 'host_vars'
            elif isinstance(entity, Group):
                subdir = 'group_vars'
            else:
                raise AnsibleParserError("Supplied entity must be Host or Group, got %s instead" % (type(entity)))

            # avoid 'chroot' type inventory hostnames /path/to/chroot
            if not entity.name.startswith(os.path.sep):
                try:
                    found_files = []
                    # load vars
                    b_opath = os.path.realpath(to_bytes(os.path.join(self._basedir, subdir)))
                    opath = to_text(b_opath)
                    key = '%s.%s' % (entity.name, opath)
                    self._display.vvvv("key: %s" % (key))
                    if cache and key in FOUND:
                        found_files = FOUND[key]
                    else:
                        # no need to do much if path does not exist for basedir
                        if os.path.exists(b_opath):
                            if os.path.isdir(b_opath):
                                self._display.debug("\tprocessing dir %s" % opath)
                                # NOTE: iterating without extension allow retriving files recursively
                                # A filter is then applied by iterating on all results and filtering by
                                # extension.
                                # See:
                                # - https://github.com/ansible-collections/community.sops/pull/6
                                found_files = loader.find_vars_files(opath, entity.name, extensions=DEFAULT_VALID_EXTENSIONS, allow_dir=False)
                                found_files.extend([file_path for file_path in loader.find_vars_files(opath, entity.name)
                                                    if any(to_text(file_path).endswith(extension) for extension in DEFAULT_VALID_EXTENSIONS)])
                                FOUND[key] = found_files
                            else:
                                self._display.warning("Found %s that is not a directory, skipping: %s" % (subdir, opath))

                    for found in found_files:
                        if cache and found in DECRYPTED:
                            file_content = DECRYPTED[found]
                        else:
                            file_content = Sops.decrypt(found, display=display, get_option_value=get_option_value)
                            DECRYPTED[found] = file_content
                        new_data = loader.load(file_content)
                        if new_data:  # ignore empty files
                            data = combine_vars(data, new_data)

                except Exception as e:
                    raise AnsibleParserError(to_native(e))

        return data
