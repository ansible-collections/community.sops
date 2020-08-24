# Community Sops Collection
[![CI](https://github.com/ansible-collections/community.sops/workflows/CI/badge.svg?event=push)](https://github.com/ansible-collections/community.sops/actions) [![Codecov](https://img.shields.io/codecov/c/github/ansible-collections/community.sops)](https://codecov.io/gh/ansible-collections/community.sops)

<!-- Describe the collection and why a user would want to use it. What does the collection do? -->
The `community.sops` collection allows integrating [`mozilla/sops`](https://github.com/mozilla/sops) in Ansible.

`mozilla/sops` is a tool for encryption and decryption of files using secure keys (GPG, KMS). It can be leveraged in Ansible to provide an easy to use and flexible to manage way to manage ecrypted secrets' files.
 
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

<!--Include some quick examples that cover the most common use cases for your collection content. -->

See [Ansible Using collections](https://docs.ansible.com/ansible/latest/user_guide/collections_using.html) for more details.

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
- testing on multiple Ansible versions

## More information

<!-- List out where the user can find additional information, such as working group meeting times, slack/IRC channels, or documentation for the product this collection automates. At a minimum, link to: -->

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/latest/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/latest/dev_guide/index.html)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/latest/community/code_of_conduct.html)

## Licensing

GNU General Public License v3.0 or later.

See [COPYING](https://www.gnu.org/licenses/gpl-3.0.txt) to see the full text.
