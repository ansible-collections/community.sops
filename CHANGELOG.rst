============================
Community Sops Release Notes
============================

.. contents:: Topics


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
