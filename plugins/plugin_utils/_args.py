# Copyright (c) 2026 Felix Fontein <felix@fontein.de>
# GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
# SPDX-License-Identifier: GPL-3.0-or-later

# Note that this module util is **PRIVATE** to the collection. It can have breaking changes at any time.
# Do not use this from other collections or standalone plugins/modules!

from __future__ import annotations

import os
import typing as t

from ansible.module_utils.common.text.converters import to_bytes as _to_bytes
from ansible.module_utils.common.validation import check_type_bool as _check_type_bool
from ansible.module_utils.common.validation import check_type_dict as _check_type_dict
from ansible.module_utils.common.validation import check_type_int as _check_type_int
from ansible.module_utils.common.validation import check_type_float as _check_type_float
from ansible.module_utils.common.validation import check_type_list as _check_type_list
from ansible.module_utils.common.validation import check_type_path as _check_type_path
from ansible.module_utils.common.validation import check_type_str as _check_type_str
from ansible.utils.path import unfrackpath as _unfrackpath

from ansible_collections.community.sops.plugins.module_utils.sops import get_sops_argument_spec as _get_sops_argument_spec

if t.TYPE_CHECKING:
    from collections.abc import Callable, Mapping


def wrap_get_option_value(
    get_option_value: Callable[[str], t.Any],
    *,
    overrides: Mapping[str, t.Any] | None = None,
) -> Callable[[str], t.Any]:
    if overrides is None:
        overrides = {}

    def new_get_option_value(option: str) -> t.Any:
        if option in overrides:
            return overrides[option]
        return get_option_value(option)

    return new_get_option_value


def wrap_get_option_value_plugin_path(
    get_option_value: Callable[[str], t.Any],
    *,
    sops_binary: t.Any,
    sops_binary_origin: str | None = "Direct",
) -> Callable[[str], t.Any]:
    if isinstance(sops_binary, str):
        candidate = sops_binary
        # ansible.config.manager.resolve_path() handles {{CWD}}:
        if "{{CWD}}" in candidate:
            candidate = candidate.replace("{{CWD}}", os.getcwd())
        basedir = sops_binary_origin if sops_binary_origin and os.path.isabs(sops_binary_origin) and os.path.exists(_to_bytes(sops_binary_origin)) else None
        candidate = _unfrackpath(candidate, follow=False, basedir=basedir)
        # ...
        if os.path.isfile(candidate):
            sops_binary = candidate
        else:
            sops_binary = os.path.expanduser(os.path.expandvars(sops_binary))
    overrides = {"sops_binary": sops_binary}
    return wrap_get_option_value(get_option_value, overrides=overrides)


def _ensure_type_impl(value: t.Any, *, option_type: str) -> t.Any:
    if option_type == "str":
        return _check_type_str(value, allow_conversion=False)
    if option_type == "dict":
        return _check_type_dict(value)
    if option_type == "bool":
        return _check_type_bool(value)
    if option_type == "int":
        return _check_type_int(value)
    if option_type == "float":
        return _check_type_float(value)
    if option_type == "path":
        return _check_type_path(_check_type_str(value, allow_conversion=False))
    raise RuntimeError(f"Unknown option type {option_type!r}")


def _ensure_type(value: t.Any, *, option_type: str, elements_type: str | None, sensitive: bool) -> t.Any:
    if value is None:
        return None
    if option_type != "list":
        return _ensure_type_impl(value, option_type=option_type)
    value = _check_type_list(value)
    if elements_type is not None:
        return [_ensure_type_impl(v, option_type=elements_type) for v in value]
    return value


def wrap_get_option_value_check_types(
    get_option_value: Callable[[str], t.Any],
    *,
    add_encrypt_specific: bool,
) -> Callable[[str], t.Any]:
    overrides: dict[str, t.Any] = {}
    for option, data in _get_sops_argument_spec(add_encrypt_specific=add_encrypt_specific).items():
        value = get_option_value(option)
        try:
            value = _ensure_type(
                value,
                option_type=data.get("type", "str"),
                elements_type=data.get("elements"),
                sensitive=data.get("no_log", False),
            )
        except TypeError as exc:
            raise ValueError(f"option {option} has invalid value: {exc}")
        overrides[option] = value
    return wrap_get_option_value(get_option_value, overrides=overrides)
