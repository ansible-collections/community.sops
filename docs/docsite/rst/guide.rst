.. _ansible_collections.community.sops.docsite.guide:

Protecting Ansible secrets with Mozilla SOPS
============================================

`Mozilla SOPS <https://github.com/mozilla/sops>`_ allows to encrypt and decrypt files using various key sources (GPG, AWS KMS, GCP KMS, ...). For structured data, such as YAML, JSON, INI and ENV files, it will encrypt values, but not mapping keys. For YAML files, it also encrypts comments. This makes it a great tool for encrypting credentials with Ansible: you can easily see which files contain which variable, but the variables themselves are encrypted.

The ability to utilize various keysources makes it easier to use in complex environments than `Ansible Vault <https://docs.ansible.com/ansible/latest/user_guide/vault.html>`_.

Setting up sops
---------------

This guide assumes that you have installed Mozilla SOPS. You can find binaries and packages `on the project's release page <https://github.com/mozilla/sops/releases>`_. Depending on your operating system, you might also be able to install it with your system's package manager.

For simplicity, you can work with GPG keys. If you do not have one, or do not want to use yours, you can run ``gpg --quick-generate-key me@example.com`` to create a GPG key for the user ID ``me@example.com``. You will need its 40 hex-digit key ID that is printed at the end. The first step is to create a ``.sops.yaml`` file in the directory tree you are working in:

.. code-block:: yaml

    creation_rules:
      - pgp: 'FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4'

Here, ``FBC7B9E2A4F9289AC0C1D4843D16CEE4A27381B4`` is the 40 hex-digit key ID. With this file you can create a sops encrypted file by running the following in the directory where ``.sops.yaml`` was placed, or a subdirectory of it:

.. code-block:: bash

    $ sops test.sops.yaml

This will open an editor window with an example YAML file. Put the following content in:

.. code-block:: yaml

    # This is a comment
    hello: world
    foo:
      - bar
      - baz

After closing the editor, sops will create ``test.sops.yaml`` with the encrypted contents:

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

You can decrypt sops-encrypted files with the :ref:`community.sops.sops lookup plugin <ansible_collections.community.sops.sops_lookup>`, and dynamically encrypt data with the :ref:`community.sops.sops_encrypt module <ansible_collections.community.sops.sops_encrypt_module>`. Being able to encrypt is useful when you create or update secrets in your Ansible playbooks.

Assume that you have an encrypted private key ``keys/private_key.pem.sops``, which was in PEM format before being encrypted by sops:

.. code-block:: bash

    $ openssl genrsa -out keys/private_key.pem 2048
    $ sops --encrypt keys/private_key.pem > keys/private_key.pem.sops
    $ wipe keys/private_key.pem

To use it in a playbook, for example to pass it to the :ref:`community.crypto.openssl_csr module <ansible_collections.community.crypto.openssl_csr_module>` to create a certificate signing request (CSR), you can use the :ref:`community.sops.sops lookup plugin <ansible_collections.community.sops.sops_lookup>` to load it:

.. code-block:: yaml+jinja

    ---
    - name: Load sops-encrypted private key
      hosts: localhost
      gather_facts: false
      tasks:
        - name: Create CSR with encrypted private key
          community.crypto.openssl_csr:
            # The private key is provided with sops:
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

    PLAY [Load sops-encrypted private key] ***************************************************************************

    TASK [Create CSR with encrypted private key] *********************************************************************
    ok: [localhost]

    PLAY RECAP *******************************************************************************************************
    localhost                  : ok=1    changed=0    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0   

Afterwards, you will have a CSR ``ansible.com.csr`` for the encrypted private key ``keys/private_key.pem.sops``.

If you want to use Ansible to generate (or update) the encrypted private key, you can use the :ref:`community.crypto.openssl_privatekey_pipe module <ansible_collections.community.crypto.openssl_privatekey_pipe_module>` to generate (or update) the private key, and use the :ref:`community.sops.sops_encrypt module <ansible_collections.community.sops.sops_encrypt_module>` to write it to disk in encrypted form:

.. code-block:: yaml+jinja

    ---
    - name: Create sops-encrypted private key
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
    - name: Create sops-encrypted private key
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

The ``empty_on_not_exist=true`` flag is needed to avoid the lookup to fail when the key does not yet exist. When this playbook is run twice, the output will be:

.. code-block:: ansible-output

    PLAY [Create sops-encrypted private key] *************************************************************************

    TASK [Create private key] ****************************************************************************************
    ok: [localhost]

    TASK [Write encrypted key to disk] *******************************************************************************
    skipping: [localhost]

    TASK [Wipe private key from Ansible's facts] *********************************************************************
    ok: [localhost]

    PLAY RECAP *******************************************************************************************************
    localhost                  : ok=2    changed=0    unreachable=0    failed=0    skipped=1    rescued=0    ignored=0   

Working with encrypted variables
--------------------------------

You can load encrypted variables similarly to the :ref:`ansible.builtin.host_group_vars vars plugin <ansible_collections.ansible.builtin.host_group_vars_vars>` with the :ref:`community.sops.sops vars plugin <ansible_collections.community.sops.sops_vars>`. If you need to load variables dynamically similarly to the :ref:`ansible.builtin.include_vars action <ansible_collections.ansible.builtin.include_vars_module>`, you can use the :ref:`community.sops.load_vars action <ansible_collections.community.sops.load_vars_module>`.

To use the vars plugin, you need to enable it in your Ansible config file (``ansible.cfg``):

.. code-block:: ini

    [default]
    vars_plugins_enabled = host_group_vars,community.sops.sops

See :ref:`VARIABLE_PLUGINS_ENABLED <VARIABLE_PLUGINS_ENABLED>` for more details on enabling vars plugins. Then you can put files with the following extensions into the ``group_vars`` and ``host_vars`` directories:

- `.sops.yaml`
- `.sops.yml`
- `.sops.json`

The vars plugin will decrypt them and you can use their unencrypted content transparently.

If you need to dynamically load encrypted variables, similar to the built-in :ref:`ansible.builtin.include_vars action <ansible_collections.ansible.builtin.include_vars_module>`, you can use the :ref:`community.sops.load_vars action <ansible_collections.community.sops.load_vars_module>` action. Please note that it is not a perfect replacement, since the built-in action relies on some hard-coded special casing in ansible-core which allows it to load the variables actually as variables (more precisely: as "unsafe" Jinja2 expressions which are automatically evaluated when used). Other action plugins, such as `community.sops.load_vars`, cannot do that and have to load the variables as facts instead.

This is mostly relevant if you use Jinja2 expressions in the encrypted variable file. When `include_vars` loads a variable file with expressions, these expressions will only be evaluated when the variable that defines them needs to be evaluated (lazy evaluation). Since `community.sops.load_vars` returns facts, it has to directly evaluate expressions at load time. (For this, set its ``expressions`` option to ``evaluate-on-load``.) This is mostly relevant if you want to refer to other variables from the same file: this will not work, since Ansible does not know the other variable yet while evaluating the first. It will only "know" them as facts after all have been evaluated and the action finishes.

For the following example, assume you hvae the encrypted file ``keys/credentials.sops.yml`` which decrypts to:

.. code-block:: yaml

    encrypted_password: foo
    expression: "{{ inventory_hostname }}"

Consider the following playbook:

.. code-block:: yaml+jinja

    ---
    - name: Create sops-encrypted private key
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

    PLAY [Create sops-encrypted private key] *************************************************************************

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

If you cange the variable loading task to:

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
