# Community Vagrant Release Notes

**Topics**

- <a href="#v1-0-1">v1\.0\.1</a>
    - <a href="#bugfixes">Bugfixes</a>
- <a href="#v1-0-0">v1\.0\.0</a>
    - <a href="#release-summary">Release Summary</a>
    - <a href="#new-modules">New Modules</a>

<a id="v1-0-1"></a>
## v1\.0\.1

<a id="bugfixes"></a>
### Bugfixes

* vagrant \- validate interface network names\, preserve interface configuration\, and render multiple interfaces correctly when options are omitted\. Backports [molecule\-plugins PR \#102](https\://github\.com/ansible\-community/molecule\-plugins/pull/102) and [molecule\-plugins PR \#374](https\://github\.com/ansible\-community/molecule\-plugins/pull/374)\.

<a id="v1-0-0"></a>
## v1\.0\.0

<a id="release-summary"></a>
### Release Summary

This is the initial release of the <code>community\.vagrant</code> collection\. It provides the <code>community\.vagrant\.vagrant</code> module\, which manages the life cycle of Vagrant instances\. The original code was taken from the <code>molecule\-vagrant</code> plugin\.

<a id="new-modules"></a>
### New Modules

* community\.vagrant\.vagrant \- Manage Vagrant instances
