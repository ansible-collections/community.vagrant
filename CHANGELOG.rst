===============================
Community Vagrant Release Notes
===============================

.. contents:: Topics

v1.0.1
======

Bugfixes
--------

- vagrant - validate interface network names, preserve interface configuration, and render multiple interfaces correctly when options are omitted. Backports `molecule-plugins PR #102 <https://github.com/ansible-community/molecule-plugins/pull/102>`_ and `molecule-plugins PR #374 <https://github.com/ansible-community/molecule-plugins/pull/374>`_.

v1.0.0
======

Release Summary
---------------

This is the initial release of the ``community.vagrant`` collection. It provides the ``community.vagrant.vagrant`` module, which manages the life cycle of Vagrant instances. The original code was taken from the ``molecule-vagrant`` plugin.

New Modules
-----------

- community.vagrant.vagrant - Manage Vagrant instances
