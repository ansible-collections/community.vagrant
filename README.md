# community.vagrant

## Code of Conduct

We follow the [Ansible Code of Conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html) in all our interactions within this project.

If you encounter abusive behavior, please refer to the [policy violations](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html#policy-violations) section of the Code for information on how to raise a complaint.

## Communication

- Join the Ansible forum:
  - [Get Help](https://forum.ansible.com/c/help/6): get help or help others. This is for questions about modules or plugins in the collection. Please add appropriate tags if you start new discussions.
  - [Social Spaces](https://forum.ansible.com/c/chat/4): gather and interact with fellow enthusiasts.
  - [News & Announcements](https://forum.ansible.com/c/news/5): track project-wide announcements including social events.

- The Ansible [Bullhorn newsletter](https://docs.ansible.com/projects/ansible/devel/community/communication.html#the-bullhorn): used to announce releases and important changes.

For more information about communication, see the [Ansible communication guide](https://docs.ansible.com/projects/ansible/devel/community/communication.html).

## Contributing to this collection

The content of this collection is made by good people just like you, a community of individuals collaborating on making the world better through developing automation software.

We are actively accepting new contributors.

All types of contributions are very welcome.

You don't know how to start? Refer to our [contribution guide](CONTRIBUTING.md)!

The current maintainers are listed in the [MAINTAINERS](MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

You can find more information in the [developer guide for collections](https://docs.ansible.com/projects/ansible/devel/dev_guide/developing_collections.html#contributing-to-collections), and in the [Ansible Community Guide](https://docs.ansible.com/projects/ansible/latest/community/index.html).

### Running tests

See [here](https://docs.ansible.com/projects/ansible/devel/dev_guide/developing_collections.html#testing-collections).

## Collection maintenance

The current maintainers are listed in the [MAINTAINERS](MAINTAINERS) file. If you have questions or need help, feel free to mention them in the proposals.

To learn how to maintain / become a maintainer of this collection, refer to the [Maintainer guidelines](MAINTAINING.md).

## Governance

<!--Describe how the collection is governed. Here can be the following text:-->

The process of decision making in this collection is based on discussing and finding consensus among participants.

Every voice is important. If you have something on your mind, create an issue or dedicated discussion and let's discuss it!

## Tested with Ansible

<!-- List the versions of Ansible the collection has been tested with. Must match what is in galaxy.yml. -->

ansible-core 2.17, 2.18, 2.19, 2.20, 2.21 and the current development version of ansible-core (`devel`).

## External requirements

<!-- List any external resources the collection depends on, for example minimum versions of an OS, libraries, or utilities. Do not list other Ansible collections here. -->

## Included content

<!-- Galaxy will eventually list the module docs within the UI, but until that is ready, you may need to either describe your plugins etc here, or point to an external docsite to cover that information. -->

## Using this collection

<!--Include some quick examples that cover the most common use cases for your collection content. It can include the following examples of installation and upgrade (change community.vagrant correspondingly):-->

### Installing the Collection from Ansible Galaxy

Before using this collection, you need to install it with the Ansible Galaxy command-line tool:

```bash
ansible-galaxy collection install community.vagrant
```

You can also include it in a `requirements.yml` file and install it with `ansible-galaxy collection install -r requirements.yml`, using the format:

```yaml
---
collections:
  - name: community.vagrant
```

Note that if you install the collection from Ansible Galaxy, it will not be upgraded automatically when you upgrade the `ansible` package. To upgrade the collection to the latest available version, run the following command:

```bash
ansible-galaxy collection install community.vagrant --upgrade
```

You can also install a specific version of the collection, for example, if you need to downgrade when something is broken in the latest version (please report an issue in this repository). Use the following syntax to install version `1.0.0`:

```bash
ansible-galaxy collection install community.vagrant:==1.0.0
```

See [Ansible Using collections](https://docs.ansible.com/ansible/devel/user_guide/collections_using.html) for more details.

## Release notes

See the [changelog](https://github.com/ansible-collections/community.vagrant/tree/main/CHANGELOG.rst).

## Release and versioning policy

The `community.vagrant` collection follows [semantic versioning](https://semver.org/). This section describes how and when the collection is released, and how deprecations are handled. Releases are planned and announced through a pinned issue in this repository and through the [Ansible community channels](#communication) (for example, The Bullhorn newsletter).

### Releasing

- New versions are released from the `main` branch. This means that new major, minor, and patch releases are all cut from `main`; if the collection ever needs to support multiple major versions side by side, this policy will be updated (for example, by switching to release branches).
- A release is made only if there are merged changes to release. Minor and patch releases are released when enough changes have accumulated; there is no fixed calendar. Major releases are released when breaking changes are required, following the deprecation cycle described below.
- A release is only made when all CI tests pass against the release commit. If they do not pass, the collection MUST NOT be released.

### Versioning

- `community.vagrant` adheres to semantic versioning:
  - **patch** releases (`x.y.z`) may only fix bugs and must not add features or deprecate anything.
  - **minor** releases (`x.y.0`) may add new features and deprecations, but must not remove anything or change the behavior of existing features.
  - **major** releases (`x.0.0`) may remove things and make breaking changes.
- The `version` in `galaxy.yml` on `main` always reflects the version currently being prepared and is bumped right after each release.
- New modules, plugins, options, and return values carry a `version_added` matching the release in which they are added.

### Deprecations

- Deprecations are tracked by version number, not by date.
- New deprecations may be added in minor releases, as long as they do not break backward compatibility.
- A deprecated feature may only be removed in the next major release after the one it was deprecated in, giving a deprecation cycle of at least one major version. Maintainers may use a longer cycle when useful.

### Changelog

- The collection uses `antsibull-changelog` to maintain its changelog.
- Every change that affects behavior (rather than only docs or tests) must have a changelog fragment, except new modules and plugins, which are auto-detected from their `version_added`.
- Changelog fragments are folded into the changelog and removed when a release is made.

### Supported ansible-core versions

- `community.vagrant` supports the ansible-core versions listed in the [meta/runtime.yml](meta/runtime.yml) (`requires_ansible`).
- ansible-core versions that have reached End of Life are dropped from the collection on an appropriate later release.

## Roadmap

None so far. If you have ideas for new features, please open an issue in this repository.

## More information

- [Ansible Collection overview](https://github.com/ansible-collections/overview)
- [Ansible User guide](https://docs.ansible.com/ansible/devel/user_guide/index.html)
- [Ansible Developer guide](https://docs.ansible.com/ansible/devel/dev_guide/index.html)
- [Ansible Collections Checklist](https://github.com/ansible-collections/overview/blob/main/collection_requirements.rst)
- [Ansible Community code of conduct](https://docs.ansible.com/ansible/devel/community/code_of_conduct.html)
- [The Bullhorn (the Ansible Contributor newsletter)](https://us19.campaign-archive.com/home/?u=56d874e027110e35dea0e03c1&id=d6635f5420)
- [News for Maintainers](https://github.com/ansible-collections/news-for-maintainers)

## Licensing

MIT.

See [LICENSE](https://opensource.org/license/mit) to see the full text.
