============================
Community Sops Release Notes
============================

.. contents:: Topics


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
