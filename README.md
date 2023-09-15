<!--
Copyright (c) Ansible Project
GNU General Public License v3.0+ (see LICENSES/GPL-3.0-or-later.txt or https://www.gnu.org/licenses/gpl-3.0.txt)
SPDX-License-Identifier: GPL-3.0-or-later
-->

# Community Sops Collection
[![CI](https://github.com/ansible-collections/community.sops/workflows/CI/badge.svg?event=push)](https://github.com/ansible-collections/community.sops/actions) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.sops)](https://codecov.io/gh/ansible-collections/community.sops)

<!-- Describe the collection and why a user would want to use it. What does the collection do? -->
The `community.sops` collection allows integrating [`getsops/sops`](https://github.com/getsops/sops) in Ansible.

`getsops/sops` is a tool for encryption and decryption of files using secure keys (GPG, KMS, age). It can be leveraged in Ansible to provide an easy to use and flexible to manage way to manage ecrypted secrets' files.

Please note that this collection does **not** support Windows targets.

**Sops version compatibility**

The following table shows which versions of sops were tested with which versions of the collection. Older (or newer) versions of sops can still work fine, it just means that we did not test them. In some cases, it could be that a minimal required version of sops is explicitly documented for a specific feature. Right now, that is not the case.

|`community.sops` version|`getsops/sops` version|
|---|---|
|0.1.0|`3.5.0+`|
|1.0.6|`3.5.0+`|
|`main` branch|`3.5.0`, `3.6.0`, `3.7.3`, `3.8.0`|

## Tested with Ansible

Tested with the current Ansible 2.9, ansible-base 2.10, ansible-core 2.11, ansible-core 2.12, ansible-core 2.13, and ansible-core 2.14 releases and the current development version of ansible-core. Ansible versions before 2.9.10 are not supported.

The vars plugin requires ansible-base 2.10 or later.

## External requirements

<!-- List any external resources the collection depends on, for example minimum versions of an OS, libraries, or utilities. Do not list other Ansible collections here. -->

You will need to install [`sops`](https://github.com/getsops/sops) manually before using plugins provided by this
collection.

## Collection Documentation

Browsing the [**latest** collection documentation](https://docs.ansible.com/ansible/latest/collections/community/sops) will show docs for the _latest version released in the Ansible package_, not the latest version of the collection released on Galaxy.

Browsing the [**devel** collection documentation](https://docs.ansible.com/ansible/devel/collections/community/sops) shows docs for the _latest version released on Galaxy_.

We also separately publish [**latest commit** collection documentation](https://ansible-collections.github.io/community.sops/branch/main/) which shows docs for the _latest commit in the `main` branch_.

If you use the Ansible package and do not update collections independently, use **latest**. If you install or update this collection directly from Galaxy, use **devel**. If you are looking to contribute, use **latest commit**.

## Included content

<!-- Galaxy will eventually list the module docs within the UI, but until that is ready, you may need to either describe your plugins etc here, or point to an external docsite to cover that information. -->

This collection provides:

- a [lookup plugin](https://docs.ansible.com/ansible/latest/user_guide/playbooks_lookups.html#playbooks-lookups) `sops` that allows looking up a sops-encrypted file content;
- a [vars plugin](https://docs.ansible.com/ansible/latest/plugins/vars.html) `sops` that allows loading Ansible vars from sops-encrypted files for hosts and groups;
- an [action plugin](https://docs.ansible.com/ansible/latest/plugins/action.html) `load_vars` that allows loading Ansible vars from a sops-encrypted file dynamically during a playbook or role;
- a [module](https://docs.ansible.com/ansible/latest/user_guide/basic_concepts.html#modules) `sops_encrypt` which allows to encrypt data with sops.
- a [role](https://docs.ansible.com/ansible/latest/user_guide/playbooks_reuse_roles.html) `install` which allows to install sops and GNU Privacy Guard.
- two [playbooks](https://docs.ansible.com/ansible/latest/user_guide/playbooks_intro.html) `install` and `install_localhost` which allow to install sops and GNU Privacy Guard.

## Using this collection

### Installing sops

To install sops, you can use the ``community.sops.install`` role. The role also installs [GNU Privacy Guard (GPG)](https://en.wikipedia.org/wiki/GNU_Privacy_Guard).

Examples:

```yaml
tasks:
  # To use the sops_encrypt module on a remote host, you need to install sops on it:
  - name: Install sops on remote hosts
    ansible.builtin.include_role:
      name: community.sops.install
    vars:
      sops_version: 2.7.0  # per default installs the latest version

  # To use the lookup plugin, filter plugin, vars plugin, or the load_vars action,
  # you need sops installed on localhost:
  - name: Install sops on localhost
    ansible.builtin.include_role:
      name: community.sops.install
    vars:
      sops_install_on_localhost: true
```

### lookup plugin

The lookup plugin can be accessed with the `community.sops.sops` key.

Examples:

```yaml
tasks:
  - name: Output secrets to screen (BAD IDEA!)
    ansible.builtin.debug:
        msg: "Content: {{ lookup('community.sops.sops', '/path/to/sops-encrypted-file.enc.yaml') }}"

  - name: Add SSH private key
    ansible.builtin.copy:
        content: "{{ lookup('community.sops.sops', user + '-id_rsa') }}"
        dest: /home/{{ user }}/.ssh/id_rsa
        owner: "{{ user }}"
        group: "{{ user }}"
        mode: 0600
    no_log: true  # avoid content to be written to log
```

See [Lookup Plugins](https://docs.ansible.com/ansible/latest/plugins/lookup.html) for more details on lookup plugins.

### filter plugin

The filter plugin can be used in Jinja2 expressions by the name `community.sops.decrypt`. It can decrypt sops-encrypted data coming from other sources than files.

Example:

```yaml
tasks:
  - name: Load sops encrypted data
    ansible.builtin.set_fact:
      encrypted_data: "{{ lookup('file', '/path/to/sops-encrypted-file.enc.yaml') }}"

  - name: Output secrets to screen (BAD IDEA!)
    ansible.builtin.debug:
      msg: "Content: {{ encrypted_data | community.sops.decrypt(output_type='yaml') }}"
```

See [Filter Plugins](https://docs.ansible.com/ansible/latest/user_guide/playbooks_filters.html) for more details on filters.

Please note that if you put a Jinja2 expression in a variable, it will be evaluated **every time it is used**. Decrypting data takes a certain amount of time. If you need to use an expression multiple times, it is better to store its evaluated form as a fact with `ansible.bulitin.set_fact` first:

```yaml
tasks:
  - name: Decrypt data once
    ansible.builtin.set_fact:
      decrypted_data: "{{ encrypted_data | community.sops.decrypt }}"
    run_once: true  # if encrypted_data is identical on all hosts

  - name: Use decrypted secrets multiple times
    ansible.builtin.openssl_privatekey:
      path: "/path/to/private_{{ item }}.pem"
      passphrase: "{{ decrypted_data }}"
      cipher: auto
    loop:
      - foo
      - bar
      - baz
```

By using `{{ encrypted_data | community.sops.decrypt }}` instead of `{{ decrypted_data }}` in the `openssl_privatekey` task, the data would be decrypted three times for every host this is executed for. With the `ansible.builtin.set_fact` and `run_once: true`, it is evaluated only once.

### vars plugin

Vars plugins only work in ansible >= 2.10 and require explicit enabling.  One
way to enable the plugin is by adding the following to the `defaults` section of
your `ansible.cfg`:

```ini
vars_plugins_enabled = host_group_vars,community.sops.sops
```

See [VARIABLE_PLUGINS_ENABLED](https://docs.ansible.com/ansible/devel/reference_appendices/config.html#variable-plugins-enabled) for more details.

After the plugin is enabled, correctly named group and host vars files will be
transparently decrypted with sops.

The files must end with one of these extensions:

* `.sops.yaml`
* `.sops.yml`
* `.sops.json`

Here is an example file structure

```
├── inventory/
│   ├── group_vars/
│   │   └── all.sops.yml
│   ├── host_vars/
│   │   ├── server1.sops.yml
│   │   └── server2/
│   │       └── data.sops.yml
│   └── hosts
├── playbooks/
│   └── setup-server.yml
└── ansible.cfg
```

You could execute the playbook in this example with the following command. The
sops vars files would be decrypted and used.

```console
$ ansible-playbook playbooks/setup-server.yml -i inventory/hosts
```

#### Determine when to load variables

Ansible 2.10 allows to determine [when vars plugins load the data](https://docs.ansible.com/ansible/latest/plugins/vars.html#using-vars-plugins).

To run the sops vars plugin right after importing inventory, you can add the following to `ansible.cfg`:

```ini
[community.sops]
vars_stage = inventory
```

#### Caching variable files

By default, the sops vars plugin caches decrypted files to avoid having to decrypt them every task. If this is not wanted, it can be explicitly disabled in `ansible.cfg`:

```ini
[community.sops]
vars_cache = false
```

Please note that when using vars plugin staging, this setting only has effect if the variables are not only loaded during the `inventory` stage. See the documentation of the `community.sops.sops` vars plugin for more details.

### load_vars action plugin

The `load_vars` action plugin can be used similarly to Ansible's `include_vars`, except that it right now only supports single files. Also, it does not allow to load proper variables (i.e. "unsafe" Jinja2 expressions which evaluate on usage), but only facts. It does allow to evaluate expressions on load-time though.

Examples:

```yaml
tasks:
  - name: Load variables from file and store them in a variable
    community.sops.load_vars:
        file: path/to/sops-encrypted-file.sops.yaml
        name: variable_to_store_contents_in

  - name: Load variables from file into global namespace, and evaluate Jinja2 expressions
    community.sops.load_vars:
        file: path/to/sops-encrypted-file-with-jinja2-expressions.sops.yaml
        # The following allows to use Jinja2 expressions in the encrypted file!
        # They are evaluated right now, i.e. not later like when loaded with include_vars.
        expressions: evaluate-on-load
```

### sops_encrypt module

The `sops_encrypt` module can be used to create and update sops encrypted files. It assumes that sops is configured via environment variables or a `.sops.yaml` file.

Examples:

```yaml
tasks:
  - name: Store secret text sops encrypted
    community.sops.sops_encrypt:
        path: path/to/sops-encrypted-file.sops
        content_text: This is some secret text.

  - name: Store secret binary data sops encrypted
    community.sops.sops_encrypt:
        path: path/to/sops-encrypted-file.sops
        content_binary: "{{ some_secret_binary_data | b64encode }}"

  - name: Store secret JSON data
    community.sops.sops_encrypt:
        path: path/to/sops-encrypted-file.sops.json
        content_json:
            key1: value1
            key2:
                - value2
                - key3: value3
                  key4: value5

  - name: Store secret YAML data
    community.sops.sops_encrypt:
        path: path/to/sops-encrypted-file.sops.yaml
        content_yaml:
            key1: value1
            key2:
                - value2
                - key3: value3
                  key4: value5
```

## Troubleshooting

### Spurious failures during encryption and decryption with gpg

Sops calls `gpg` with `--use-agent`. When running multiple of these in parallel, for example when loading variables or looking up files for various hosts at once, some of these can randomly fail with messages such as
```
Failed to get the data key required to decrypt the SOPS file.

Group 0: FAILED
  D13xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx: FAILED
    - | could not decrypt data key with PGP key:
      | golang.org/x/crypto/openpgp error: Reading PGP message
      | failed: openpgp: incorrect key; GPG binary error: exit
      | status 2

  828xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx: FAILED
    - | could not decrypt data key with PGP key:
      | golang.org/x/crypto/openpgp error: Reading PGP message
      | failed: openpgp: incorrect key; GPG binary error: exit
      | status 2

Recovery failed because no master key was able to decrypt the file. In
order for SOPS to recover the file, at least one key has to be successful,
but none were.
```
This is a limitation of gpg-agent which can be fixed by adding `auto-expand-secmem` to `~/.gnupg/gpg-agent.conf` ([reference on option](https://www.gnupg.org/documentation/manuals/gnupg/Agent-Options.html#index-ssh_002dfingerprint_002ddigest), [reference on config file](https://www.gnupg.org/documentation/manuals/gnupg/Agent-Configuration.html)).

(See https://github.com/ansible-collections/community.sops/issues/34 and https://dev.gnupg.org/T4146 for more details.)

## Contributing to this collection

<!--Describe how the community can contribute to your collection. At a minimum, include how and where users can create issues to report problems or request features for this collection.  List contribution requirements, including preferred workflows and necessary testing, so you can benefit from community PRs. If you are following general Ansible contributor guidelines, you can link to - [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html). -->

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## Release notes

See [CHANGELOG.rst](https://github.com/ansible-collections/community.sops/blob/main/CHANGELOG.rst).

## Releasing, Versioning and Deprecation

This collection follows [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

We plan to regularly release new minor or bugfix versions once new features or bugfixes have been implemented.

Releasing the current major version happens from the `main` branch. We will create a `stable-1` branch for 1.x.y versions once we start working on a 2.0.0 release, to allow backporting bugfixes and features from the 2.0.0 branch (`main`) to `stable-1`. A `stable-2` branch will be created once we work on a 3.0.0 release, and so on.

We currently are not planning any deprecations or new major releases like 2.0.0 containing backwards incompatible changes. If backwards incompatible changes are needed, we plan to deprecate the old behavior as early as possible. We also plan to backport at least bugfixes for the old major version for some time after releasing a new major version. We will not block community members from backporting other bugfixes and features from the latest stable version to older release branches, under the condition that these backports are of reasonable quality.

### TODO

- add a role providing sops installation (with version pinning)
- a full test suite

## Code of Conduct

This repository adheres to the [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)

## Licensing

This collection is primarily licensed and distributed as a whole under the GNU General Public License v3.0 or later.

See [LICENSES/GPL-3.0-or-later.txt](https://github.com/ansible-collections/community.sops/blob/main/COPYING) for the full text.

Parts of the collection are licensed under the [BSD 2-Clause license](https://github.com/ansible-collections/community.sops/blob/main/LICENSES/BSD-2-Clause.txt).

All files have a machine readable `SDPX-License-Identifier:` comment denoting its respective license(s) or an equivalent entry in an accompanying `.license` file. Only changelog fragments (which will not be part of a release) are covered by a blanket statement in `.reuse/dep5`. This conforms to the [REUSE specification](https://reuse.software/spec/).
