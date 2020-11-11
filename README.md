# Community Sops Collection
[![CI](https://github.com/ansible-collections/community.sops/workflows/CI/badge.svg?event=push)](https://github.com/ansible-collections/community.sops/actions) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.sops)](https://codecov.io/gh/ansible-collections/community.sops)

<!-- Describe the collection and why a user would want to use it. What does the collection do? -->
The `community.sops` collection allows integrating [`mozilla/sops`](https://github.com/mozilla/sops) in Ansible.

`mozilla/sops` is a tool for encryption and decryption of files using secure keys (GPG, KMS). It can be leveraged in Ansible to provide an easy to use and flexible to manage way to manage ecrypted secrets' files.

**Sops version compatibility**

The following table shows which versions of sops were tested with which versions of the collection. Older (or newer) versions of sops can still work fine, it just means that we did not test them. In some cases, it could be that a minimal required version of sops is explicitly documented for a specific feature. Right now, that is not the case.

|`community.sops` version|`mozilla/sops` version|
|---|---|
|0.1.0|`3.6.1+`|
|`main` branch|`3.6.1+`|

## Tested with Ansible

<!-- List the versions of Ansible the collection has been tested with. Must match what is in galaxy.yml. -->

- `devel`
- latest 2.9 release
- latest 2.10 release

## External requirements

<!-- List any external resources the collection depends on, for example minimum versions of an OS, libraries, or utilities. Do not list other Ansible collections here. -->

You will need to install [`sops`](https://github.com/mozilla/sops) manually before using plugins provided by this
collection.

## Included content

<!-- Galaxy will eventually list the module docs within the UI, but until that is ready, you may need to either describe your plugins etc here, or point to an external docsite to cover that information. -->

This collection provides:

- a `lookup` plugin that allows looking up a sops-encrypted file content
- a `vars` plugin that allows loading Ansible vars from a sops-encrypted file

## Using this collection

### lookup plugin

The lookup plugin can be accessed with the `community.sops.sops` key.

Examples:

```
tasks:
  - name: Output secrets to screen (BAD IDEA!)
    debug:
        msg: "Content: {{ lookup('community.sops.sops', '/path/to/sops-encrypted-file.enc.yaml') }}"

  - name: Add SSH private key
    copy:
        content: "{{ lookup('community.sops.sops', user + '-id_rsa') }}"
        dest: /home/{{ user }}/.ssh/id_rsa
        owner: "{{ user }}"
        group: "{{ user }}"
        mode: 0600
    no_log: true  # avoid content to be written to log
```

See [Lookup Plugins](https://docs.ansible.com/ansible/latest/plugins/lookup.html) for more details on lookup plugins


### vars plugin

Vars plugins only work in ansible >= 2.10 and require explicit enabling.  One
way to enable the plugin is by adding the following to the `default` section of
your `ansible.cfg`:

```
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

```
[community.sops]
vars_stage = inventory
```

#### Caching variable files

By default, the sops vars plugin caches decrypted files to avoid having to decrypt them every task. If this is not wanted, it can be explicitly disabled in `ansible.cfg`:

```
[community.sops]
vars_cache = false
```

### load_vars action plugin

The `load_vars` action plugin can be used similarly to Ansible's `include_vars`, except that it right now only supports single files. Also, it does not allow to load proper variables (i.e. "unsafe" Jinja2 expressions which evaluate on usage), but only facts. It does allow to evaluate expressions on load-time though.

Examples:

```
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

### encrypt_sops module

The `encrypt_sops` module can be used to create and update sops encrypted files. It assumes that sops is configured via environment variables or a `.sops.yaml` file.

Examples:

```
tasks:
  - name: Store secret text sops encrypted
    community.sops.encrypt_sops:
        path: path/to/sops-encrypted-file.sops
        content_text: This is some secret text.

  - name: Store secret binary data sops encrypted
    community.sops.encrypt_sops:
        path: path/to/sops-encrypted-file.sops
        content_binary: "{{ some_secret_binary_data | b64encode }}"

  - name: Store secret JSON data
    community.sops.encrypt_sops:
        path: path/to/sops-encrypted-file.sops.json
        content_json:
            key1: value1
            key2:
                - value2
                - key3: value3
                  key4: value5

  - name: Store secret YAML data
    community.sops.encrypt_sops:
        path: path/to/sops-encrypted-file.sops.yaml
        content_yaml:
            key1: value1
            key2:
                - value2
                - key3: value3
                  key4: value5
```

## Contributing to this collection

<!--Describe how the community can contribute to your collection. At a minimum, include how and where users can create issues to report problems or request features for this collection.  List contribution requirements, including preferred workflows and necessary testing, so you can benefit from community PRs. If you are following general Ansible contributor guidelines, you can link to - [Ansible Community Guide](https://docs.ansible.com/ansible/latest/community/index.html). -->

See [CONTRIBUTING.md](./CONTRIBUTING.md)

## Release notes

See [CHANGELOG.rst](https://github.com/ansible-collections/community.sops/blob/main/CHANGELOG.rst).

## Roadmap

<!-- Optional. Include the roadmap for this collection, and the proposed release/versioning strategy so users can anticipate the upgrade/update cycle. -->

Ansible Collections are required to adhere to [Semantic Versioning](https://semver.org/). More details on versioning can be found [in the Ansible docs](https://docs.ansible.com/ansible/latest/dev_guide/developing_collections.html#collection-versions).

### TODO

- add a role providing sops installation (with version pinning)
- a full test suite

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
