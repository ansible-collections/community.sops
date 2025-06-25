..
  Copyright (c) Ansible Project
  GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
  SPDX-License-Identifier: GPL-3.0-or-later

.. _ansible_collections.community.sops.docsite.guide:

Protecting Ansible secrets with SOPS
====================================

`CNCF SOPS <https://github.com/getsops/sops>`_ allows to encrypt and decrypt files using various key sources (GPG, AWS KMS, GCP KMS, ...). For structured data, such as YAML, JSON, INI and ENV files, it will encrypt values, but not mapping keys. For YAML files, it also encrypts comments. This makes it a great tool for encrypting credentials with Ansible: you can easily see which files contain which variable, but the variables themselves are encrypted.

The ability to utilize various keysources makes it easier to use in complex environments than :ref:`Ansible Vault <vault_guide_index>`.

.. contents::
   :local:
   :depth: 1

Installing SOPS
---------------

You can find binaries and packages `on the project's release page <https://github.com/getsops/sops/releases>`_. Depending on your operating system, you might also be able to install it with your system's package manager.

This collection provides a :ansplugin:`role community.sops.install <community.sops.install#role>` which allows to install SOPS and `GNU Privacy Guard (GPG) <https://en.wikipedia.org/wiki/GNU_Privacy_Guard>`__. The role allows to install SOPS from the system's package manager or from GitHub; see :ansopt:`community.sops.install#role:main:sops_source` for details. Both SOPS and GPG can be installed on the remote hosts or the Ansible controller; see :ansopt:`community.sops.install#role:main:sops_install_on_localhost` for details.

.. code-block:: yaml

    - name: Playbook to install SOPS
      hosts: all
      tasks:
        # To use the sops_encrypt module on a remote host, you need to install SOPS on it:
        - name: Install SOPS on remote hosts
          ansible.builtin.include_role:
            name: community.sops.install
          vars:
            sops_version: 2.7.0  # per default installs the latest version

        # To use the lookup plugin, filter plugin, vars plugin, or the load_vars action,
        # you need SOPS installed on localhost:
        - name: Install SOPS on localhost
          ansible.builtin.include_role:
            name: community.sops.install
          vars:
            sops_install_on_localhost: true

When using ansible-core 2.11 or later, you can also use two convenience playbooks:

.. code-block:: console

    # Install SOPS on Ansible controller
    $ ansible-playbook community.sops.install_localhost

    # Install SOPS on remote servers
    $ ansible-playbook community.sops.install --inventory /path/to/inventory

Installing community.sops in an Execution Environment
-----------------------------------------------------

When building an execution environment containing community.sops, please note that by default SOPS is not automatically installed. This is due to a limitation of the dependency specification system for execution environments. If you are building an execution environment that contains community.sops, you should make sure that SOPS is installed in it.

The simplest way of ensuring this is to use the ``community.sops.install_localhost`` playbook. When defining an execution environment, you can add a ``RUN`` additional build step to your ``execution-environment.yml``:

.. code-block:: yaml

    ---
    version: 3
    dependencies:
      galaxy: requirements.yml
    additional_build_steps:
      append_final:
        # Ensure that SOPS is installed in the EE, assuming the EE is for ansible-core 2.11 or newer
        - RUN ansible-playbook -v community.sops.install_localhost

Note that this only works if the execution environment is built with ansible-core 2.11 or newer. When using an execution environment with Ansible 2.9, you have to use the :ansplugin:`community.sops.install#role` role manually. Also note that you need to make sure that Ansible 2.9 uses the correct Python interpreter to be able to install system packages with; in the below example we are assuming a RHEL/CentOS based execution environment base image:

.. code-block:: yaml

    ---
    version: 3
    dependencies:
      galaxy: requirements.yml
    additional_build_steps:
      append_final:
        # Special step needed for Ansible 2.9 based EEs
        - >-
          RUN ansible localhost -m include_role -a name=community.sops.install
              -e sops_install_on_localhost=true
              -e ansible_python_interpreter=/usr/libexec/platform-python

Once this step has been taken care of, you can use all plugins and modules (on ``localhost``) from community.sops in the execution environment.

Setting up SOPS
---------------

From now on this guide assumes that you have installed SOPS.

For simplicity, you can work with GPG keys. If you do not have one, or do not want to use yours, you can run ``gpg --quick-generate-key me@example.com`` to create a GPG key for the user ID ``me@example.com``. You will need its 40 hex-digit key ID that is printed at the end. The first step is to create a ``.sops.yaml`` file in the directory tree you are working in:

.. code-block:: yaml

    creation_rules:
      - pgp: 'FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4'

Here, ``FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4`` is the 40 hex-digit key ID. With this file you can create a SOPS-encrypted file by running the following in the directory where ``.sops.yaml`` was placed, or a subdirectory of it:

.. code-block:: console

    $ sops test.sops.yaml

This will open an editor window with an example YAML file. Put the following content in:

.. code-block:: yaml

    # This is a comment
    hello: world
    foo:
      - bar
      - baz

After closing the editor, SOPS will create ``test.sops.yaml`` with the encrypted contents:

.. code-block:: yaml

    #ENC[AES256_GCM,data:r6Ok05DzzHBO4tonlz2t49CF,iv:Y0P39iXwaGYU9NG5oRC3NuaGVL40uruSze0CxbDTpTk=,tag:EzoG+X+BJAHbxE0asSyGlQ==,type:comment]
    hello: ENC[AES256_GCM,data:onBZqWk=,iv:bwj4bwaeh3vpVDYqY2AnYo1thF955i5vbFpCC1DwJtM=,tag:4qbVzuHTaPrXm64r2Rqz1Q==,type:str]
    foo:
        - ENC[AES256_GCM,data:UsY8,iv:USv71rKfvbTF+3a5T2WO56wGVu609/0uigqkO0pa6U4=,tag:s8NdqLp+8OOQg4xDfE78oA==,type:str]
        - ENC[AES256_GCM,data:Dhmo,iv:qWs5gN2SCXYq0EfGelZhODsdViKB9w2taQMhsqy0D2g=,tag:I+ZFvuxnsvQmywqz+a/M9w==,type:str]
    sops:
        kms: []
        gcp_kms: []
        azure_kv: []
        hc_vault: []
        age: []
        lastmodified: "2021-06-15T19:36:34Z"
        mac: ENC[AES256_GCM,data:HAvLeOvt7xWI7B5TCeDEsL6sOSzGGeTbgBSJaZkwadmoAm3Ny4IZPF8JAbFaPPLmN8FJVAt4D61aIWa6Xwi3xMj1g6DmxFfgK6JFJqWqW122UlMhqZ/WuMWFV6yVxpTLDXgemndgGDJqUTUi14FMh/MzPDg4f6kFP64kA9fpLrY=,iv:LdhswnMymZG8J9na/jnF3WYnX0DvzvoBlvjUCu4nI6c=,tag:Qt4d7L3FXsgfmg9iOs8P4A==,type:str]
        pgp:
            - created_at: "2021-06-15T19:36:01Z"
              enc: |-
                -----BEGIN PGP MESSAGE-----

                wcBMAyUpShfNkFB/AQgAT8OAKnWLBQRG3kT5lZCmyoPzK6RwF0zRkwCzJkLNl6xg
                nQjUjpD03ZD4FtiRidspXEj7NvCLDghJ0UETtDjmrwsTeJ5YAK/JxouWmoNhVVdF
                p0qOlj/THXIV+ypVaqrisZGZiTqeWjUNFuayknvjm3XduOOPZA1MIJ14pQxcgca4
                NWmKwPwXTWEy3RJ0ZsnjjjYvKHjHyvbHdbDgARu8R1jEgdNPKPBRVpEY6RNeafXI
                gFBVRfrhPKD6HmnmNvjHwUc/K+wOa1ciIYVrT4mPXoyBsFkyV0egh/QRf0JO8+X7
                Ut/jEtCrl9BXJCNYGmC5EU3PPiFlAu1MRxlCiPNWltLmASn2w62wMpgih6f+OpI/
                zyEOdz0qx80LEfhv3+jBbDfBwz4GqpAHUr0fCXDzeDiKfzlU6isagoIAhJfwX6oG
                NeQ47ktk1XhPmgIwxxuvonG14iQoU2cA
                =GoXQ
                -----END PGP MESSAGE-----
              fp: FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4
        unencrypted_suffix: _unencrypted
        version: 3.7.1

The first line contains the encrypted content. The second line contains the unencrypted key of ``hello: world``, and the encrypted string value ``world``. The next few lines contain the unencrypted key ``foo`` with the encrypted list elements.

At the end, the ``sops`` section contains metadata, which includes the private key needed to decrypt the file encrypted with the public key of the GPG key ID ``FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4``. If you had multiple GPG keys configured, or also other key sources, you can also find the file secret key encrypted with these keys here.

Working with encrypted files
----------------------------

You can decrypt SOPS-encrypted files with the :ansplugin:`community.sops.sops lookup plugin <community.sops.sops#lookup>`, and dynamically encrypt data with the :ansplugin:`community.sops.sops_encrypt module <community.sops.sops_encrypt#module>`. Being able to encrypt is useful when you create or update secrets in your Ansible playbooks.

Assume that you have an encrypted private key ``keys/private_key.pem.sops``, which was in PEM format before being encrypted by SOPS:

.. code-block:: console

    $ openssl genrsa -out keys/private_key.pem 2048
    $ sops --encrypt keys/private_key.pem > keys/private_key.pem.sops
    $ wipe keys/private_key.pem

To use it in a playbook, for example to pass it to the :ansplugin:`community.crypto.openssl_csr module <community.crypto.openssl_csr#module>` to create a certificate signing request (CSR), you can use the :ansplugin:`community.sops.sops lookup plugin <community.sops.sops#lookup>` to load it:

.. code-block:: yaml+jinja

    ---
    - name: Load SOPS-encrypted private key
      hosts: localhost
      gather_facts: false
      tasks:
        - name: Create CSR with encrypted private key
          community.crypto.openssl_csr:
            # The private key is provided with SOPS:
            privatekey_content: "{{ lookup('community.sops.sops', 'keys/private_key.pem.sops') }}"
            # Store the CSR on disk unencrypted:
            path: ansible.com.csr
            # This is going to be a CSR for ansible.com and www.ansible.com
            subject_alt_name:
              - DNS:ansible.com
              - DNS:www.ansible.com
            use_common_name_for_san: false

This results in the following output:

.. code-block:: ansible-output

    PLAY [Load SOPS-encrypted private key] ***************************************************************************

    TASK [Create CSR with encrypted private key] *********************************************************************
    ok: [localhost]

    PLAY RECAP *******************************************************************************************************
    localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Afterwards, you will have a CSR ``ansible.com.csr`` for the encrypted private key ``keys/private_key.pem.sops``.

If you want to use Ansible to generate (or update) the encrypted private key, you can use the :ansplugin:`community.crypto.openssl_privatekey_pipe module <community.crypto.openssl_privatekey_pipe#module>` to generate (or update) the private key, and use the :ansplugin:`community.sops.sops_encrypt module <community.sops.sops_encrypt#module>` to write it to disk in encrypted form:

.. code-block:: yaml+jinja

    ---
    - name: Create SOPS-encrypted private key
      hosts: localhost
      gather_facts: false
      tasks:
        - block:
            - name: Create private key
              community.crypto.openssl_privatekey_pipe:
                size: 2048
              no_log: true  # Always use this with openssl_privatekey_pipe!
              register: private_key

            - name: Write encrypted key to disk
              community.sops.sops_encrypt:
                path: keys/private_key.pem.sops
                content_text: "{{ private_key.privatekey }}"

          always:
            - name: Wipe private key from Ansible's facts
              # This is particularly important if the playbook doesn't end here!
              set_fact:
                private_key: ''

This playbook creates a new key on every run. If you want the private key creation to be idempotent, you need to do a little more work:

.. code-block:: yaml+jinja

    ---
    - name: Create SOPS-encrypted private key
      hosts: localhost
      gather_facts: false
      tasks:
        - block:
            - name: Create private key
              community.crypto.openssl_privatekey_pipe:
                size: 2048
                content: >-
                  {{ lookup(
                        'community.sops.sops',
                        'keys/private_key.pem.sops',
                        empty_on_not_exist=true
                     ) }}
              no_log: true  # Always use this with openssl_privatekey_pipe!
              register: private_key

            - name: Write encrypted key to disk
              community.sops.sops_encrypt:
                path: keys/private_key.pem.sops
                content_text: "{{ private_key.privatekey }}"
              when: private_key is changed

          always:
            - name: Wipe private key from Ansible's facts
              # This is particularly important if the playbook doesn't end here!
              set_fact:
                private_key: ''

The :ansopt:`community.sops.sops#lookup:empty_on_not_exist=true` flag is needed to avoid the lookup to fail when the key does not yet exist. When this playbook is run twice, the output will be:

.. code-block:: ansible-output

    PLAY [Create SOPS-encrypted private key] *************************************************************************

    TASK [Create private key] ****************************************************************************************
    ok: [localhost]

    TASK [Write encrypted key to disk] *******************************************************************************
    skipping: [localhost]

    TASK [Wipe private key from Ansible's facts] *********************************************************************
    ok: [localhost]

    PLAY RECAP *******************************************************************************************************
    localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0

Working with encrypted data from other sources
----------------------------------------------

You can use the :ansplugin:`community.sops.decrypt Jinja2 filter <community.sops.decrypt#filter>` to decrypt arbitrary data. This can be data read earlier from a file, returned from an action, or obtained through some other means.

For example, assume that you want to decrypt a file retrieved from a HTTPS server with the :ansplugin:`ansible.builtin.uri module <ansible.builtin.uri#module>`. To use the :ansplugin:`community.sops.sops lookup <community.sops.sops#lookup>`, you have to write it to a file first. With the filter, you can directly decrypt it:

.. code-block:: yaml+jinja

    ---
    - name: Decrypt file fetched from URL
      hosts: localhost
      gather_facts: false
      tasks:
        - name: Fetch file from URL
          ansible.builtin.uri:
            url: https://raw.githubusercontent.com/getsops/sops/master/functional-tests/res/comments.enc.yaml
            return_content: true
          register: encrypted_content

        - name: Show encrypted data
          debug:
            msg: "{{ encrypted_content.content | ansible.builtin.from_yaml }}"

        - name: Decrypt data and decode decrypted YAML
          set_fact:
            decrypted_data: "{{ encrypted_content.content | community.sops.decrypt | ansible.builtin.from_yaml }}"

        - name: Show decrypted data
          debug:
            msg: "{{ decrypted_data }}"

The output will be:

.. code-block:: ansible-output

    PLAY [Decrypt file fetched from URL] *****************************************************************************

    TASK [Fetch file from URL] ***************************************************************************************
    ok: [localhost]

    TASK [Show encrypted data] ***************************************************************************************
    ok: [localhost] => {
        "msg": {
            "dolor": "ENC[AES256_GCM,data:IgvT,iv:wtPNYbDTARFE810PH6ldOLzCDcAjkB/dzPsZjpgHcko=,tag:zwE8P+AwO1hrHkgF6pTbZw==,type:str]",
            "lorem": "ENC[AES256_GCM,data:PhmSdTs=,iv:J5ugEWq6RfyNx+5zDXvcTdoQ18YYZkqesDED7LNzou4=,tag:0Qrom6J6aUnZMZzGz5XCxw==,type:str]",
            "sops": {
                "age": [],
                "azure_kv": [],
                "gcp_kms": [],
                "hc_vault": [],
                "kms": [],
                "lastmodified": "2020-10-07T15:49:13Z",
                "mac": "ENC[AES256_GCM,data:2dhyKdHYSynjXPwYrn9356wA7vRKw+T5qwBenI2vZrgthpQBOCQG4M6f7eeH3VLTxB4mN4CAchb25dsNRoGr6A38VruaSSAhPco3Rh4AlvKSvXuhgRnzZvNxE/bnHX1D4K5cdTb4FsJg/Ue1l7UcWrlrv1s3H3SwLHP/nf+suD0=,iv:6xBYURjjaQzlUOKOrs2NWOChiNFZVAGPJZQZ59MwX3o=,tag:uXD5VYme+c8eHcCc5TD2YA==,type:str]",
                "pgp": [
                    {
                        "created_at": "2019-08-29T21:52:32Z",
                        "enc": "-----BEGIN PGP MESSAGE-----\n\nhQEMAyUpShfNkFB/AQgAlvpTj0NYqF4mQyIeM7wX2SHLb4U07/flpqDpp2W/30Pz\nAHA7sYrgP0l8BrjT2kwtgCN0cdfoIHJudezrNjANp2P5TbP2b9kYYNxpehzB9PFj\nFixnCS7Zp8WIt1yXr1TX+ANZoXLopVcRbMaQ5OdH7CN1pNQtMR+R3FR3X/IqKxiU\nDo1YLaooRJICUC8LJw2Tb4K+lYnTSqd/HalLGym++ivFvdDB1Ya1GhT1FswXidXK\nIRjsOVbxV0q5VeNOR0zxsheOvuHyCje16c7NXJtATJVWtTFABJB8u7CY5HhZSgq+\nrXJHyLHqVLzJ8E4WqHQkMNUlVcrqAz7glZ6xbAhfI9JeAYk5SuBOQOQ4yvASqH4K\nb0N3+/abluBY7YPqKuRZBiEtmcYlZ+zIHuOTP1rD/7L5VY8CwE5U8SFlEqwM7nQJ\n6/vtl6qngOFjwt34WrhZzUfLPB/wRV/m1Qv2kr0RNA==\n=Ykiw\n-----END PGP MESSAGE-----\n",
                        "fp": "FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4"
                    }
                ],
                "unencrypted_suffix": "_unencrypted",
                "version": "3.6.1"
            }
        }
    }

    TASK [Decrypt data] **********************************************************************************************
    ok: [localhost]

    TASK [Show decrypted data] ***************************************************************************************
    ok: [localhost] => {
        "msg": {
            "dolor": "sit",
            "lorem": "ipsum"
        }
    }

    PLAY RECAP *******************************************************************************************************
    localhost                  : ok=4    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

Please note that if you put a Jinja2 expression in a variable, it will be evaluated **every time it is used**. Decrypting data takes a certain amount of time. If you need to use an expression multiple times, it is better to store its evaluated form as a fact with :ansplugin:`ansible.bulitin.set_fact <ansible.builtin.set_fact#module>` first. This can be important if decrypted data should be passed to a role

.. code-block:: yaml+jinja

    ---
    - name: Decrypt file fetched from URL
      hosts: localhost
      gather_facts: false
      tasks:
        - name: Fetch file from URL
          ansible.builtin.uri:
            url: https://raw.githubusercontent.com/getsops/sops/master/functional-tests/res/comments.enc.yaml
            return_content: true
          register: encrypted_content

        # BAD: every time the role uses decrypted_data, the data will be decrypted!

        - name: Call role with decrypted data
          include_role:
            name: myrole
          vars:
            role_parameter: "{{ encrypted_content.content | community.sops.decrypt | ansible.builtin.from_yaml }}"

        # GOOD: the data is decrypted once before the role is called,

        - name: Store decrypted data as fact
          set_fact:
            decrypted_data: "{{ encrypted_content.content | community.sops.decrypt | ansible.builtin.from_yaml }}"

        - name: Call role with decrypted data
          include_role:
            name: myrole
          vars:
            role_parameter: "{{ decrypted_data }}"

Working with encrypted variables
--------------------------------

You can load encrypted variables similarly to the :ansplugin:`ansible.builtin.host_group_vars vars plugin <ansible.builtin.host_group_vars#vars>` with the :ansplugin:`community.sops.sops vars plugin <community.sops.sops#vars>`. If you need to load variables dynamically similarly to the :ansplugin:`ansible.builtin.include_vars action <ansible.builtin.include_vars#module>`, you can use the :ansplugin:`community.sops.load_vars action <community.sops.load_vars#module>`.

To use the vars plugin, you need to enable it in your Ansible config file (``ansible.cfg``):

.. code-block:: ini

    [defaults]
    vars_plugins_enabled = host_group_vars,community.sops.sops

See :ref:`VARIABLE_PLUGINS_ENABLED <VARIABLE_PLUGINS_ENABLED>` for more details on enabling vars plugins. Then you can put files with the following extensions into the ``group_vars`` and ``host_vars`` directories:

- ``.sops.yaml``
- ``.sops.yml``
- ``.sops.json``

(The list of extensions can be adjusted with :ansopt:`community.sops.sops#vars:valid_extensions`.) The vars plugin will decrypt them and you can use their unencrypted content transparently.

If you need to dynamically load encrypted variables, similar to the built-in :ansplugin:`ansible.builtin.include_vars action <ansible.builtin.include_vars#module>`, you can use the :ansplugin:`community.sops.load_vars action <community.sops.load_vars#module>` action. Please note that it is not a perfect replacement, since the built-in action relies on some hard-coded special casing in ansible-core which allows it to load the variables actually as variables (more precisely: as "unsafe" Jinja2 expressions which are automatically evaluated when used). Other action plugins, such as :ansplugin:`community.sops.load_vars#module`, cannot do that and have to load the variables as facts instead.

This is mostly relevant if you use Jinja2 expressions in the encrypted variable file. When :ansplugin:`ansible.builtin.include_vars#module` loads a variable file with expressions, these expressions will only be evaluated when the variable that defines them needs to be evaluated (lazy evaluation). Since :ansplugin:`community.sops.load_vars#module` returns facts, it has to directly evaluate expressions at load time. (For this, set its :ansopt:`community.sops.load_vars#module:expressions` option to :ansval:`evaluate-on-load`.) This is mostly relevant if you want to refer to other variables from the same file: this will not work, since Ansible does not know the other variable yet while evaluating the first. It will only "know" them as facts after all have been evaluated and the action finishes.

For the following example, assume you have the encrypted file ``keys/credentials.sops.yml`` which decrypts to:

.. code-block:: yaml

    encrypted_password: foo
    expression: "{{ inventory_hostname }}"

Consider the following playbook:

.. code-block:: yaml+jinja

    ---
    - name: Create SOPS-encrypted private key
      hosts: localhost
      gather_facts: false
      tasks:
        - name: Load encrypted credentials
          community.sops.load_vars:
            file: keys/credentials.sops.yml
            expressions: ignore  # explicitly do not evaluate expressions
                                 # on load (this is the default)

        - name: Show password
          debug:
            msg: "The password is {{ encrypted_password }}"

        - name: Show expression
          debug:
            msg: "The expression is {{ expression }}"

Running it produces:

.. code-block:: ansible-output

    PLAY [Create SOPS-encrypted private key] *************************************************************************

    TASK [Load encrypted credentials] ********************************************************************************
    ok: [localhost]

    TASK [Show password] *********************************************************************************************
    ok: [localhost] => {
        "msg": "The password is foo"
    }

    TASK [Show expression] *******************************************************************************************
    ok: [localhost] => {
        "msg": "The expression is {{ inventory_hostname }}"
    }

    PLAY RECAP *******************************************************************************************************
    localhost                  : ok=3    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0

If you change the variable loading task to:

.. code-block:: yaml+jinja

        - name: Load encrypted credentials
          community.sops.load_vars:
            file: keys/credentials.sops.yml
            expressions: evaluate-on-load

The last task will now show the evaluated expression:

.. code-block:: ansible-output

    TASK [Show expression] *******************************************************************************************
    ok: [localhost] => {
        "msg": "The expression is localhost"
    }
