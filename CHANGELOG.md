# Community Sops Release Notes

**Topics**
- <a href="#v1-6-7">v1\.6\.7</a>
  - <a href="#release-summary">Release Summary</a>
  - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-6-6">v1\.6\.6</a>
  - <a href="#release-summary-1">Release Summary</a>
  - <a href="#bugfixes-1">Bugfixes</a>
- <a href="#v1-6-5">v1\.6\.5</a>
  - <a href="#release-summary-2">Release Summary</a>
  - <a href="#bugfixes-2">Bugfixes</a>
- <a href="#v1-6-4">v1\.6\.4</a>
  - <a href="#release-summary-3">Release Summary</a>
  - <a href="#bugfixes-3">Bugfixes</a>
- <a href="#v1-6-3">v1\.6\.3</a>
  - <a href="#release-summary-4">Release Summary</a>
  - <a href="#known-issues">Known Issues</a>
- <a href="#v1-6-2">v1\.6\.2</a>
  - <a href="#release-summary-5">Release Summary</a>
  - <a href="#bugfixes-4">Bugfixes</a>
- <a href="#v1-6-1">v1\.6\.1</a>
  - <a href="#release-summary-6">Release Summary</a>
  - <a href="#bugfixes-5">Bugfixes</a>
- <a href="#v1-6-0">v1\.6\.0</a>
  - <a href="#release-summary-7">Release Summary</a>
  - <a href="#minor-changes">Minor Changes</a>
- <a href="#v1-5-0">v1\.5\.0</a>
  - <a href="#release-summary-8">Release Summary</a>
  - <a href="#minor-changes-1">Minor Changes</a>
  - <a href="#new-playbooks">New Playbooks</a>
  - <a href="#new-roles">New Roles</a>
- <a href="#v1-4-1">v1\.4\.1</a>
  - <a href="#release-summary-9">Release Summary</a>
  - <a href="#bugfixes-6">Bugfixes</a>
- <a href="#v1-4-0">v1\.4\.0</a>
  - <a href="#release-summary-10">Release Summary</a>
  - <a href="#minor-changes-2">Minor Changes</a>
- <a href="#v1-3-0">v1\.3\.0</a>
  - <a href="#release-summary-11">Release Summary</a>
  - <a href="#minor-changes-3">Minor Changes</a>
- <a href="#v1-2-3">v1\.2\.3</a>
  - <a href="#release-summary-12">Release Summary</a>
- <a href="#v1-2-2">v1\.2\.2</a>
  - <a href="#release-summary-13">Release Summary</a>
  - <a href="#bugfixes-7">Bugfixes</a>
- <a href="#v1-2-1">v1\.2\.1</a>
  - <a href="#release-summary-14">Release Summary</a>
- <a href="#v1-2-0">v1\.2\.0</a>
  - <a href="#release-summary-15">Release Summary</a>
  - <a href="#minor-changes-4">Minor Changes</a>
  - <a href="#bugfixes-8">Bugfixes</a>
- <a href="#v1-1-0">v1\.1\.0</a>
  - <a href="#release-summary-16">Release Summary</a>
  - <a href="#minor-changes-5">Minor Changes</a>
  - <a href="#new-plugins">New Plugins</a>
    - <a href="#filter">Filter</a>
- <a href="#v1-0-6">v1\.0\.6</a>
  - <a href="#release-summary-17">Release Summary</a>
  - <a href="#bugfixes-9">Bugfixes</a>
- <a href="#v1-0-5">v1\.0\.5</a>
  - <a href="#release-summary-18">Release Summary</a>
  - <a href="#bugfixes-10">Bugfixes</a>
- <a href="#v1-0-4">v1\.0\.4</a>
  - <a href="#release-summary-19">Release Summary</a>
  - <a href="#security-fixes">Security Fixes</a>
- <a href="#v1-0-3">v1\.0\.3</a>
  - <a href="#release-summary-20">Release Summary</a>
  - <a href="#bugfixes-11">Bugfixes</a>
- <a href="#v1-0-2">v1\.0\.2</a>
  - <a href="#release-summary-21">Release Summary</a>
- <a href="#v1-0-1">v1\.0\.1</a>
  - <a href="#release-summary-22">Release Summary</a>
- <a href="#v1-0-0">v1\.0\.0</a>
  - <a href="#release-summary-23">Release Summary</a>
  - <a href="#minor-changes-6">Minor Changes</a>
- <a href="#v0-2-0">v0\.2\.0</a>
  - <a href="#release-summary-24">Release Summary</a>
  - <a href="#minor-changes-7">Minor Changes</a>
- <a href="#v0-1-0">v0\.1\.0</a>
  - <a href="#release-summary-25">Release Summary</a>
  - <a href="#new-plugins-1">New Plugins</a>
    - <a href="#lookup">Lookup</a>
    - <a href="#vars">Vars</a>
  - <a href="#new-modules">New Modules</a>

<a id="v1-6-7"></a>
## v1\.6\.7

<a id="release-summary"></a>
### Release Summary

Bugfix release\.

<a id="bugfixes"></a>
### Bugfixes

* sops\_encrypt \- ensure that output\-type is set to <code>yaml</code> when the file extension <code>\.yml</code> is used\. Now both <code>\.yaml</code> and <code>\.yml</code> files use the SOPS <code>\-\-output\-type\=yaml</code> formatting \([https\://github\.com/ansible\-collections/community\.sops/issues/164](https\://github\.com/ansible\-collections/community\.sops/issues/164)\)\.

<a id="v1-6-6"></a>
## v1\.6\.6

<a id="release-summary-1"></a>
### Release Summary

Make fully compatible with and test against sops 3\.8\.0\.

<a id="bugfixes-1"></a>
### Bugfixes

* Fix RPM URL for the 3\.8\.0 release \([https\://github\.com/ansible\-collections/community\.sops/pull/161](https\://github\.com/ansible\-collections/community\.sops/pull/161)\)\.

<a id="v1-6-5"></a>
## v1\.6\.5

<a id="release-summary-2"></a>
### Release Summary

Make compatible with and test against sops 3\.8\.0\-rc\.1\.

<a id="bugfixes-2"></a>
### Bugfixes

* Avoid pre\-releases when picking the latest version when using the GitHub API method \([https\://github\.com/ansible\-collections/community\.sops/pull/159](https\://github\.com/ansible\-collections/community\.sops/pull/159)\)\.
* Fix changed DEB and RPM URLs for 3\.8\.0 and its prerelease\(s\) \([https\://github\.com/ansible\-collections/community\.sops/pull/159](https\://github\.com/ansible\-collections/community\.sops/pull/159)\)\.

<a id="v1-6-4"></a>
## v1\.6\.4

<a id="release-summary-3"></a>
### Release Summary

Maintenance/bugfix release for the move of sops to the new [getsops GitHub organization](https\://github\.com/getsops)\.

<a id="bugfixes-3"></a>
### Bugfixes

* install role \- fix <code>sops\_github\_latest\_detection\=latest\-release</code>\, which broke due to sops moving to another GitHub organization \([https\://github\.com/ansible\-collections/community\.sops/pull/151](https\://github\.com/ansible\-collections/community\.sops/pull/151)\)\.

<a id="v1-6-3"></a>
## v1\.6\.3

<a id="release-summary-4"></a>
### Release Summary

Maintenance release with updated documentation\.

From this version on\, community\.sops is using the new [Ansible semantic markup](https\://docs\.ansible\.com/ansible/devel/dev\_guide/developing\_modules\_documenting\.html\#semantic\-markup\-within\-module\-documentation)
in its documentation\. If you look at documentation with the ansible\-doc CLI tool
from ansible\-core before 2\.15\, please note that it does not render the markup
correctly\. You should be still able to read it in most cases\, but you need
ansible\-core 2\.15 or later to see it as it is intended\. Alternatively you can
look at [the devel docsite](https\://docs\.ansible\.com/ansible/devel/collections/community/sops/)
for the rendered HTML version of the documentation of the latest release\.

<a id="known-issues"></a>
### Known Issues

* Ansible markup will show up in raw form on ansible\-doc text output for ansible\-core before 2\.15\. If you have trouble deciphering the documentation markup\, please upgrade to ansible\-core 2\.15 \(or newer\)\, or read the HTML documentation on [https\://docs\.ansible\.com/ansible/devel/collections/community/sops/](https\://docs\.ansible\.com/ansible/devel/collections/community/sops/)\.

<a id="v1-6-2"></a>
## v1\.6\.2

<a id="release-summary-5"></a>
### Release Summary

Maintenance release\.

<a id="bugfixes-4"></a>
### Bugfixes

* install role \- make sure that the <code>pkg\_mgr</code> fact is definitely available when installing on <code>localhost</code>\. This can improve error messages in some cases \([https\://github\.com/ansible\-collections/community\.sops/issues/145](https\://github\.com/ansible\-collections/community\.sops/issues/145)\, [https\://github\.com/ansible\-collections/community\.sops/pull/146](https\://github\.com/ansible\-collections/community\.sops/pull/146)\)\.

<a id="v1-6-1"></a>
## v1\.6\.1

<a id="release-summary-6"></a>
### Release Summary

Maintenance release\.

<a id="bugfixes-5"></a>
### Bugfixes

* action plugin helper \- fix handling of deprecations for ansible\-core 2\.14\.2 \([https\://github\.com/ansible\-collections/community\.sops/pull/136](https\://github\.com/ansible\-collections/community\.sops/pull/136)\)\.
* various plugins \- remove unnecessary imports \([https\://github\.com/ansible\-collections/community\.sops/pull/133](https\://github\.com/ansible\-collections/community\.sops/pull/133)\)\.

<a id="v1-6-0"></a>
## v1\.6\.0

<a id="release-summary-7"></a>
### Release Summary

Feature release improving the installation role\.

<a id="minor-changes"></a>
### Minor Changes

* install role \- add <code>sops\_github\_latest\_detection</code> option that allows to configure which method to use for detecting the latest release on GitHub\. By default \(<code>auto</code>\) first tries to retrieve a list of recent releases using the API\, and if that fails due to rate limiting\, tries to obtain the latest GitHub release from a semi\-documented URL \([https\://github\.com/ansible\-collections/community\.sops/pull/133](https\://github\.com/ansible\-collections/community\.sops/pull/133)\)\.
* install role \- add <code>sops\_github\_token</code> option to allow passing a GitHub token\. This can for example be used to avoid rate limits when using the role in GitHub Actions \([https\://github\.com/ansible\-collections/community\.sops/pull/132](https\://github\.com/ansible\-collections/community\.sops/pull/132)\)\.
* install role \- implement another method to determine the latest release on GitHub than using the GitHub API\, which can make installation fail due to rate\-limiting \([https\://github\.com/ansible\-collections/community\.sops/pull/131](https\://github\.com/ansible\-collections/community\.sops/pull/131)\)\.

<a id="v1-5-0"></a>
## v1\.5\.0

<a id="release-summary-8"></a>
### Release Summary

Feature release\.

<a id="minor-changes-1"></a>
### Minor Changes

* Automatically install GNU Privacy Guard \(GPG\) in execution environments\. To install Mozilla sops a manual step needs to be added to the EE definition\, see the collection\'s documentation for details \([https\://github\.com/ansible\-collections/community\.sops/pull/98](https\://github\.com/ansible\-collections/community\.sops/pull/98)\)\.

<a id="new-playbooks"></a>
### New Playbooks

* community\.sops\.install \- Installs sops and GNU Privacy Guard on all remote hosts
* community\.sops\.install\_localhost \- Installs sops and GNU Privacy Guard on localhost

<a id="new-roles"></a>
### New Roles

* community\.sops\.install \- Install Mozilla sops

<a id="v1-4-1"></a>
## v1\.4\.1

<a id="release-summary-9"></a>
### Release Summary

Maintenance release to improve compatibility with future ansible\-core releases\.

<a id="bugfixes-6"></a>
### Bugfixes

* load\_vars \- ensure compatibility with newer versions of ansible\-core \([https\://github\.com/ansible\-collections/community\.sops/pull/121](https\://github\.com/ansible\-collections/community\.sops/pull/121)\)\.

<a id="v1-4-0"></a>
## v1\.4\.0

<a id="release-summary-10"></a>
### Release Summary

Feature release\.

<a id="minor-changes-2"></a>
### Minor Changes

* Allow to specify age keys as <code>age\_key</code>\, or age keyfiles as <code>age\_keyfile</code> \([https\://github\.com/ansible\-collections/community\.sops/issues/116](https\://github\.com/ansible\-collections/community\.sops/issues/116)\, [https\://github\.com/ansible\-collections/community\.sops/pull/117](https\://github\.com/ansible\-collections/community\.sops/pull/117)\)\.
* sops\_encrypt \- allow to specify age recipients \([https\://github\.com/ansible\-collections/community\.sops/issues/116](https\://github\.com/ansible\-collections/community\.sops/issues/116)\, [https\://github\.com/ansible\-collections/community\.sops/pull/117](https\://github\.com/ansible\-collections/community\.sops/pull/117)\)\.

<a id="v1-3-0"></a>
## v1\.3\.0

<a id="release-summary-11"></a>
### Release Summary

Feature release\.

<a id="minor-changes-3"></a>
### Minor Changes

* All software licenses are now in the <code>LICENSES/</code> directory of the collection root\, and the collection repository conforms to the [REUSE specification](https\://reuse\.software/spec/) except for the changelog fragments \([https\://github\.com/ansible\-collections/community\.crypto/sops/108](https\://github\.com/ansible\-collections/community\.crypto/sops/108)\, [https\://github\.com/ansible\-collections/community\.sops/pull/113](https\://github\.com/ansible\-collections/community\.sops/pull/113)\)\.
* sops vars plugin \- added a configuration option to temporarily disable the vars plugin \([https\://github\.com/ansible\-collections/community\.sops/pull/114](https\://github\.com/ansible\-collections/community\.sops/pull/114)\)\.

<a id="v1-2-3"></a>
## v1\.2\.3

<a id="release-summary-12"></a>
### Release Summary

Fix formatting bug in documentation\. No code changes\.

<a id="v1-2-2"></a>
## v1\.2\.2

<a id="release-summary-13"></a>
### Release Summary

Maintenance release\.

<a id="bugfixes-7"></a>
### Bugfixes

* Include <code>simplified\_bsd\.txt</code> license file for the <code>sops</code> module utils\.

<a id="v1-2-1"></a>
## v1\.2\.1

<a id="release-summary-14"></a>
### Release Summary

Maintenance release with updated documentation\.

<a id="v1-2-0"></a>
## v1\.2\.0

<a id="release-summary-15"></a>
### Release Summary

Collection release for inclusion in Ansible 4\.9\.0 and 5\.1\.0\.

This release contains a change allowing to configure generic plugin options with ansible\.cfg keys and env variables\.

<a id="minor-changes-4"></a>
### Minor Changes

* sops lookup and vars plugin \- allow to configure almost all generic options by ansible\.cfg entries and environment variables \([https\://github\.com/ansible\-collections/community\.sops/pull/81](https\://github\.com/ansible\-collections/community\.sops/pull/81)\)\.

<a id="bugfixes-8"></a>
### Bugfixes

* Fix error handling in calls of the <code>sops</code> binary when negative errors are returned \([https\://github\.com/ansible\-collections/community\.sops/issues/82](https\://github\.com/ansible\-collections/community\.sops/issues/82)\, [https\://github\.com/ansible\-collections/community\.sops/pull/83](https\://github\.com/ansible\-collections/community\.sops/pull/83)\)\.

<a id="v1-1-0"></a>
## v1\.1\.0

<a id="release-summary-16"></a>
### Release Summary

A minor release for inclusion in Ansible 4\.2\.0\.

<a id="minor-changes-5"></a>
### Minor Changes

* Avoid internal ansible\-core module\_utils in favor of equivalent public API available since at least Ansible 2\.9 \([https\://github\.com/ansible\-collections/community\.sops/pull/73](https\://github\.com/ansible\-collections/community\.sops/pull/73)\)\.

<a id="new-plugins"></a>
### New Plugins

<a id="filter"></a>
#### Filter

* community\.sops\.decrypt \- Decrypt sops\-encrypted data

<a id="v1-0-6"></a>
## v1\.0\.6

<a id="release-summary-17"></a>
### Release Summary

This release makes the collection compatible to the latest beta release of ansible\-core 2\.11\.

<a id="bugfixes-9"></a>
### Bugfixes

* action\_module plugin helper \- make compatible with latest changes in ansible\-core 2\.11\.0b3 \([https\://github\.com/ansible\-collections/community\.sops/pull/58](https\://github\.com/ansible\-collections/community\.sops/pull/58)\)\.
* community\.sops\.load\_vars \- make compatible with latest changes in ansible\-core 2\.11\.0b3 \([https\://github\.com/ansible\-collections/community\.sops/pull/58](https\://github\.com/ansible\-collections/community\.sops/pull/58)\)\.

<a id="v1-0-5"></a>
## v1\.0\.5

<a id="release-summary-18"></a>
### Release Summary

This release fixes a bug that prevented correct YAML file to be created when the output was ending in <em class="title-reference">\.yaml</em>\.

<a id="bugfixes-10"></a>
### Bugfixes

* community\.sops\.sops\_encrypt \- use output type <code>yaml</code> when path ends with <code>\.yaml</code> \([https\://github\.com/ansible\-collections/community\.sops/pull/56](https\://github\.com/ansible\-collections/community\.sops/pull/56)\)\.

<a id="v1-0-4"></a>
## v1\.0\.4

<a id="release-summary-19"></a>
### Release Summary

This is a security release\, fixing a potential information leak in the <code>community\.sops\.sops\_encrypt</code> module\.

<a id="security-fixes"></a>
### Security Fixes

* community\.sops\.sops\_encrypt \- mark the <code>aws\_secret\_access\_key</code> and <code>aws\_session\_token</code> parameters as <code>no\_log</code> to avoid leakage of secrets \([https\://github\.com/ansible\-collections/community\.sops/pull/54](https\://github\.com/ansible\-collections/community\.sops/pull/54)\)\.

<a id="v1-0-3"></a>
## v1\.0\.3

<a id="release-summary-20"></a>
### Release Summary

This release include some fixes to Ansible docs and required changes for inclusion in Ansible\.

<a id="bugfixes-11"></a>
### Bugfixes

* community\.sops\.sops lookup plugins \- fix wrong format of Ansible variables so that these are actually used \([https\://github\.com/ansible\-collections/community\.sops/pull/51](https\://github\.com/ansible\-collections/community\.sops/pull/51)\)\.
* community\.sops\.sops vars plugins \- remove non\-working Ansible variables \([https\://github\.com/ansible\-collections/community\.sops/pull/51](https\://github\.com/ansible\-collections/community\.sops/pull/51)\)\.

<a id="v1-0-2"></a>
## v1\.0\.2

<a id="release-summary-21"></a>
### Release Summary

Fix of 1\.0\.1 release which had no changelog entry\.

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="release-summary-22"></a>
### Release Summary

Re\-release of 1\.0\.0 to counteract error during release\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary-23"></a>
### Release Summary

First stable release\. This release is expected to be included in Ansible 3\.0\.0\.

<a id="minor-changes-6"></a>
### Minor Changes

* All plugins and modules\: allow to pass generic sops options with new options <code>config\_path</code>\, <code>enable\_local\_keyservice</code>\, <code>keyservice</code>\. Also allow to pass AWS parameters with options <code>aws\_profile</code>\, <code>aws\_access\_key\_id</code>\, <code>aws\_secret\_access\_key</code>\, and <code>aws\_session\_token</code> \([https\://github\.com/ansible\-collections/community\.sops/pull/47](https\://github\.com/ansible\-collections/community\.sops/pull/47)\)\.
* community\.sops\.sops\_encrypt \- allow to pass encryption\-specific options <code>kms</code>\, <code>gcp\_kms</code>\, <code>azure\_kv</code>\, <code>hc\_vault\_transit</code>\, <code>pgp</code>\, <code>unencrypted\_suffix</code>\, <code>encrypted\_suffix</code>\, <code>unencrypted\_regex</code>\, <code>encrypted\_regex</code>\, <code>encryption\_context</code>\, and <code>shamir\_secret\_sharing\_threshold</code> to sops \([https\://github\.com/ansible\-collections/community\.sops/pull/47](https\://github\.com/ansible\-collections/community\.sops/pull/47)\)\.

<a id="v0-2-0"></a>
## v0\.2\.0

<a id="release-summary-24"></a>
### Release Summary

This release adds features for the lookup and vars plugins\.

<a id="minor-changes-7"></a>
### Minor Changes

* community\.sops\.sops lookup plugin \- add <code>empty\_on\_not\_exist</code> option which allows to return an empty string instead of an error when the file does not exist \([https\://github\.com/ansible\-collections/community\.sops/pull/33](https\://github\.com/ansible\-collections/community\.sops/pull/33)\)\.
* community\.sops\.sops vars plugin \- add option to control caching \([https\://github\.com/ansible\-collections/community\.sops/pull/32](https\://github\.com/ansible\-collections/community\.sops/pull/32)\)\.
* community\.sops\.sops vars plugin \- add option to determine when vars are loaded \([https\://github\.com/ansible\-collections/community\.sops/pull/32](https\://github\.com/ansible\-collections/community\.sops/pull/32)\)\.

<a id="v0-1-0"></a>
## v0\.1\.0

<a id="release-summary-25"></a>
### Release Summary

First release of the <em class="title-reference">community\.sops</em> collection\!
This release includes multiple plugins\: an <em class="title-reference">action</em> plugin\, a <em class="title-reference">lookup</em> plugin and a <em class="title-reference">vars</em> plugin\.

<a id="new-plugins-1"></a>
### New Plugins

<a id="lookup"></a>
#### Lookup

* community\.sops\.sops \- Read sops encrypted file contents

<a id="vars"></a>
#### Vars

* community\.sops\.sops \- Loading sops\-encrypted vars files

<a id="new-modules"></a>
### New Modules

* community\.sops\.load\_vars \- Load sops\-encrypted variables from files\, dynamically within a task
* community\.sops\.sops\_encrypt \- Encrypt data with sops
