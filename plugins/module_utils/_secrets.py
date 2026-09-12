# Copyright (c) 2026 Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

from __future__ import absolute_import, division, print_function
__metaclass__ = type


try:
    from collections.abc import Sequence, Mapping
    string_type = str
except ImportError:
    # Python 2 compat
    # pylint: disable-next=ansible-bad-import-from
    from collections import Sequence, Mapping  # type: ignore[attr-defined]
    # pylint: disable-next=undefined-variable
    string_type = unicode  # type: ignore[misc,name-defined]


try:
    from ansible.module_utils.secrets import register_secret  # type: ignore[import-not-found]
    HAS_SECRETS_API = True
except ImportError:
    HAS_SECRETS_API = False


def _mark_recursively(value):
    if isinstance(value, Mapping):
        return {k: _mark_recursively(v) for k, v in value.items()}
    if isinstance(value, string_type):
        return register_secret(value)
    if isinstance(value, Sequence):
        return [_mark_recursively(v) for v in value]
    return value


def mark_values_as_secrets(value):
    """Register all strings appearing in the (potentially nested) data structure value secrets."""
    if HAS_SECRETS_API:
        value = _mark_recursively(value)
    return value


def mark_as_secret(value):  # type: (string_type) -> string_type
    """Register a string as a secret."""
    if HAS_SECRETS_API:
        value = register_secret(value)
    return value
