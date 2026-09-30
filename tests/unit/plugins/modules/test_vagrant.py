# Copyright (c) 2026 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for the vagrant module."""

from __future__ import annotations

from copy import deepcopy
from typing import Any

import jinja2
import pytest
from ansible_collections.community.internal_test_tools.tests.unit.plugins.modules.utils import (
    AnsibleFailJson,
    fail_json,
)

from ansible_collections.community.vagrant.plugins.modules import (
    vagrant as vagrant_module,
)


class FakeModule:
    """Provide the AnsibleModule attributes used by VagrantClient."""

    def __init__(self) -> None:
        self.params = {
            "default_box": "generic/alpine316",
            "provider_name": "virtualbox",
        }

    def fail_json(self, **kwargs: Any) -> None:
        """Raise a test-visible exception for an Ansible module failure."""
        fail_json(**kwargs)

    def warn(self, message: str) -> None:
        """Ignore compatibility warnings in unit tests."""


def make_client() -> vagrant_module.VagrantClient:
    """Construct a VagrantClient without invoking external Vagrant commands."""
    client = object.__new__(vagrant_module.VagrantClient)
    client._module = FakeModule()  # pylint: disable=protected-access
    client.cachier = "machine"
    client.provision = False
    return client


def render_vagrantfile(instances: list[dict[str, Any]]) -> str:
    """Render the module's Vagrantfile template using production settings."""
    environment = jinja2.Environment(
        autoescape=True,
        trim_blocks=True,
        lstrip_blocks=True,
    )
    template = environment.from_string(vagrant_module.VAGRANTFILE_TEMPLATE)
    return template.render(instances=instances, cachier=None, no_kvm=False)


def test_interfaces_render_as_separate_statements_with_optional_options() -> None:
    """Render each interface on its own line and omit an empty options argument."""
    instance = {
        "name": "instance",
        "interfaces": [
            {"network_name": "private_network"},
            {
                "network_name": "forwarded_port",
                "guest": 22,
                "host": 2222,
            },
        ],
    }

    config = make_client()._get_instance_vagrant_config_dict(  # pylint: disable=protected-access
        deepcopy(instance),
    )
    rendered = render_vagrantfile([config])
    network_lines = [
        line.strip() for line in rendered.splitlines() if "c.vm.network" in line
    ]

    assert network_lines == [
        'c.vm.network "private_network"',
        'c.vm.network "forwarded_port", guest: 22, host: 2222',
    ]


def test_interface_requires_network_name() -> None:
    """Reject an interface without a network name."""
    with pytest.raises(AnsibleFailJson) as exc:
        make_client()._get_instance_vagrant_config_dict(  # pylint: disable=protected-access
            {"name": "instance", "interfaces": [{"guest": 22}]},
        )

    assert exc.value.args[0]["msg"] == "Each interface must have a 'network_name' key."


def test_interface_rejects_unsupported_network_name() -> None:
    """Reject an interface with an unsupported Vagrant network name."""
    with pytest.raises(AnsibleFailJson) as exc:
        make_client()._get_instance_vagrant_config_dict(  # pylint: disable=protected-access
            {"name": "instance", "interfaces": [{"network_name": "unsupported"}]},
        )

    assert exc.value.args[0]["msg"] == "Invalid network_name value unsupported."


def test_interface_normalization_does_not_mutate_input() -> None:
    """Keep the caller's interface mapping unchanged during normalization."""
    instance = {
        "name": "instance",
        "interfaces": [{"network_name": "forwarded_port", "guest": 22, "host": 2222}],
    }
    original = deepcopy(instance)

    make_client()._get_instance_vagrant_config_dict(  # pylint: disable=protected-access
        instance,
    )

    assert instance == original


def test_interface_without_options_omits_options() -> None:
    """Omit the options key when an interface has no Vagrant options."""
    config = make_client()._get_instance_vagrant_config_dict(  # pylint: disable=protected-access
        {"name": "instance", "interfaces": [{"network_name": "private_network"}]},
    )

    assert config["networks"] == [{"name": "private_network"}]
