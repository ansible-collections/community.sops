============================
Community Sops Release Notes
============================

.. contents:: Topics


v1.0.4
======

Release Summary
---------------

This is a security release, fixing a potential information leak in the ``sops_encrypt`` module.

Security Fixes
--------------

- sops_encrypt - mark the ``aws_secret_access_key`` and ``aws_session_token`` parameters as ``no_log`` to avoid leakage of secrets (https://github.com/ansible-collections/community.sops/pull/54).

v1.0.3
======

Release Summary
---------------

This release include some fixes to Ansible docs and required changes for inclusion in Ansible.

Bugfixes
--------

- sops lookup plugins - fix wrong format of Ansible variables so that these are actually used (https://github.com/ansible-collections/community.sops/pull/51).
- sops vars plugins - remove non-working Ansible variables (https://github.com/ansible-collections/community.sops/pull/51).

v1.0.2
======

Release Summary
---------------

Fix of 1.0.1 release which had no changelog entry.

v1.0.1
======

Release Summary
---------------

Re-release of 1.0.0 to counteract error during release.

v1.0.0
======

Release Summary
---------------

First stable release. This release is expected to be included in Ansible 3.0.0.

Minor Changes
-------------

- All plugins and modules: allow to pass generic sops options with new options ``config_path``, ``enable_local_keyservice``, ``keyservice``. Also allow to pass AWS parameters with options ``aws_profile``, ``aws_access_key_id``, ``aws_secret_access_key``, and ``aws_session_token`` (https://github.com/ansible-collections/community.sops/pull/47).
- sops_encrypt - allow to pass encryption-specific options ``kms``, ``gcp_kms``, ``azure_kv``, ``hc_vault_transit``, ``pgp``, ``unencrypted_suffix``, ``encrypted_suffix``, ``unencrypted_regex``, ``encrypted_regex``, ``encryption_context``, and ``shamir_secret_sharing_threshold`` to sops (https://github.com/ansible-collections/community.sops/pull/47).

v0.2.0
======

Release Summary
---------------

This release adds features for the lookup and vars plugins.

Minor Changes
-------------

- sops lookup plugin - add ``empty_on_not_exist`` option which allows to return an empty string instead of an error when the file does not exist (https://github.com/ansible-collections/community.sops/pull/33).
- sops vars plugin - add option to control caching (https://github.com/ansible-collections/community.sops/pull/32).
- sops vars plugin - add option to determine when vars are loaded (https://github.com/ansible-collections/community.sops/pull/32).

v0.1.0
======

Release Summary
---------------

First release of the `community.sops` collection!
This release includes multiple plugins: an `action` plugin, a `lookup` plugin and a `vars` plugin.


New Plugins
-----------

Lookup
~~~~~~

- sops - Read sops encrypted file contents

Vars
~~~~

- sops - Loading sops-encrypted vars files

New Modules
-----------

- load_vars - Load sops-encrypted variables from files, dynamically within a task
- sops_encrypt - Encrypt data with sops
