# Copyright: (c) 2020, Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

from __future__ import (absolute_import, division, print_function)
__metaclass__ = type

from os import path, walk
import re

from ansible.module_utils.common.validation import check_type_bool, check_type_str
from ansible.module_utils.common._collections_compat import Sequence, Mapping
from ansible.module_utils.six import iteritems, string_types
from ansible.module_utils._text import to_native, to_text
from ansible.plugins.action import ActionBase
from ansible.utils.display import Display

from ansible_collections.community.sops.plugins.module_utils.sops import Sops, SopsError

display = Display()


class ActionModule(ActionBase):

    _VALID_ARGS = frozenset(['file', 'name', 'expressions'])

    def _load(self, filename):
        def get_option_value(argument_name):
            # TODO
            return None

        output = Sops.decrypt(filename, display=display, get_option_value=get_option_value)

        data = self._loader.load(output, file_name=filename, show_content=False)
        if not data:
            data = dict()
        if not isinstance(data, dict):
            # Should not happen with sops-encrypted files
            raise Exception('{0} must be stored as a dictionary/hash'.format(to_native(filename)))
        return data

    def _get_option(self, name, type_name, default=None, accept_none=False):
        value = self._task.args.get(name)
        if value is None:
            if accept_none:
                return value
            elif default is not None:
                value = default
            else:
                raise Exception("Option %s must be specified" % name)
        checkers = {
            'str': lambda v: check_type_str(v, allow_conversion=False),
            'bool': check_type_bool,
        }
        try:
            return checkers[type_name](value)
        except TypeError as e:
            msg = "Value for option %s" % name
            msg += " is of type %s and we were unable to convert to %s: %s" % (type(value), type_name, to_native(e))
            raise Exception(msg)

    def _evaluate(self, value):
        if isinstance(value, string_types):
            # must come *before* Sequence, as strings are also instances of Sequence
            return self._templar.template(value)
        if isinstance(value, Sequence):
            return [self._evaluate(v) for v in value]
        if isinstance(value, Mapping):
            return dict((k, self._evaluate(v)) for k, v in iteritems(value))
        return value

    def run(self, tmp=None, task_vars=None):
        """ Load yml files recursively from a directory.
        """
        del tmp  # tmp no longer has any effect

        result = super(ActionModule, self).run(task_vars=task_vars)

        try:
            file = to_text(self._get_option('file', 'str'))
            name = self._get_option('name', 'str', accept_none=True)
            if name is not None:
                name = to_text(name)
            expressions = self._get_option('expressions', 'str', default='ignore')
            if expressions not in ('ignore', 'evaluate-on-load'):
                raise Exception('"expressions" must be one of "ignore" and "evaluate-on-load"')
        except Exception as e:
            result['failed'] = True
            result['message'] = to_text(e)
            return result

        data = dict()
        files = []
        try:
            filename = self._find_needle('vars', file)
            data.update(self._load(filename))
            files.append(filename)
        except Exception as e:
            result['failed'] = True
            result['message'] = to_native(e)
            return result

        if name is None:
            value = data
        else:
            value = dict()
            value[name] = data

        if expressions == 'evaluate-on-load':
            value = self._evaluate(value)

        result['ansible_included_var_files'] = files
        result['ansible_facts'] = value
        result['_ansible_no_log'] = True

        return result
