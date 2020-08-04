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

import os
from ansible import constants as C
from ansible.errors import AnsibleParserError
from ansible.module_utils._text import to_bytes, to_native, to_text
from ansible.plugins.vars import BaseVarsPlugin
from ansible.inventory.host import Host
from ansible.inventory.group import Group
from ansible.utils.vars import combine_vars
from ansible_collections.community.sops.plugins.module_utils.sops import Sops, SopsError

from ansible.utils.display import Display
display = Display()


DOCUMENTATION = '''
    vars: sops_vars
    author: Edoardo Tenani (@endorama) <e.tenani@arduino.cc>
    short_description: Loading sops-encrypted vars files
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
'''


def find_vars_files(self, path, name, extensions=None, allow_dir=True):
    """
    Find vars files in a given path with specified name. This will find
    files in a dir named <name>/ or a file called <name> ending in known
    extensions.
    """

    b_path = to_bytes(os.path.join(path, name))
    found = []

    if extensions is None:
        # Look for file with no extension first to find dir before file
        extensions = [''] + C.YAML_FILENAME_EXTENSIONS
    # add valid extensions to name
    for ext in extensions:

        if '.' in ext:
            full_path = b_path + to_bytes(ext)
        elif ext:
            full_path = b'.'.join([b_path, to_bytes(ext)])
        else:
            full_path = b_path

        if self.path_exists(full_path):
            if self.is_directory(full_path):
                if allow_dir:
                    found.extend(_get_dir_vars_files(self, to_text(full_path), extensions))
                else:
                    continue
            else:
                found.append(full_path)
            break

    if allow_dir and ('' not in extensions):
        if self.path_exists(b_path) and self.is_directory(b_path):
            found.extend(_get_dir_vars_files(self, to_text(b_path), extensions))

    return found


def _get_dir_vars_files(self, path, extensions):
    display.vvvv("Checking directory %s" % path)
    found = []
    for spath in sorted(self.list_directory(path)):
        display.vvvv("spath: %s" % spath)
        if not spath.startswith(u'.') and not spath.endswith(u'~'):  # skip hidden and backups

            ext = os.path.splitext(spath)[-1]
            full_spath = os.path.join(path, spath)

            if self.is_directory(full_spath) and not ext:  # recursive search if dir
                found.extend(self._get_dir_vars_files(full_spath, extensions))
            elif self.is_file(full_spath) and (not ext or to_text(full_spath).endswith(tuple(extensions))):
                # only consider files with valid extensions or no extension
                found.append(full_spath)

    return found


FOUND = {}
DECRYPTED = {}
DEFAULT_VALID_EXTENSIONS = [".sops.yaml", ".sops.yml", ".sops.json"]

class VarsModule(BaseVarsPlugin):

    def get_vars(self, loader, path, entities, cache=True):
        ''' parses the inventory file '''

        if not isinstance(entities, list):
            entities = [entities]

        super(VarsModule, self).get_vars(loader, path, entities)

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
                                found_files = find_vars_files(loader, opath, entity.name, extensions=DEFAULT_VALID_EXTENSIONS, allow_dir=True)
                                FOUND[key] = found_files
                            else:
                                self._display.warning("Found %s that is not a directory, skipping: %s" % (subdir, opath))

                    for found in found_files:
                        if cache and found in DECRYPTED:
                            file_content = DECRYPTED[found]
                        else:
                            file_content = Sops.decrypt(found, display=display)
                            DECRYPTED[found] = file_content
                        new_data = loader.load(file_content)
                        if new_data:  # ignore empty files
                            data = combine_vars(data, new_data)

                except Exception as e:
                    raise AnsibleParserError(to_native(e))

        return data
