# Copyright (c) 2026 Ansible Project
# GNU General Public License v3.0+ (see COPYING or https://www.gnu.org/licenses/gpl-3.0.txt)

"""Unit tests for the vagrant module."""

from __future__ import annotations

from copy import deepcopy
from typing import Any
from unittest.mock import Mock

import jinja2
import pytest
from ansible_collections.community.internal_test_tools.tests.unit.plugins.modules.utils import (
    AnsibleExitJson,
    AnsibleFailJson,
    exit_json,
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
            "instance_name": None,
            "provider_name": None,
        }

    def exit_json(self, **kwargs: Any) -> None:
        """Raise a test-visible exception for a successful module exit."""
        exit_json(**kwargs)

    def fail_json(self, **kwargs: Any) -> None:
        """Raise a test-visible exception for an Ansible module failure."""
        fail_json(**kwargs)

    def warn(self, message: str) -> None:
        """Ignore compatibility warnings in unit tests."""


def make_client(
    provider_name: str | None = "virtualbox",
) -> vagrant_module.VagrantClient:
    """Construct a VagrantClient without invoking external Vagrant commands."""
    client = object.__new__(vagrant_module.VagrantClient)
    client._module = FakeModule()  # pylint: disable=protected-access
    module = getattr(client, "_module")
    module.params["provider_name"] = provider_name
    client.cachier = "machine"
    client.provision = False
    client._has_error = None  # pylint: disable=protected-access
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


def make_up_client(
    provider_name: str | None,
    monkeypatch: pytest.MonkeyPatch,
) -> vagrant_module.VagrantClient:
    """Construct a client with the lifecycle dependencies stubbed."""
    client = make_client()
    module = getattr(client, "_module")
    module.params["provider_name"] = provider_name
    client.instances = [{"name": "instance"}]
    client._vagrant = Mock()  # pylint: disable=protected-access
    monkeypatch.setattr(client, "_running", Mock(return_value=0))
    monkeypatch.setattr(client, "_conf", Mock(return_value=[]))
    client._config = {"workdir": "/tmp"}  # pylint: disable=protected-access
    return client


def test_provider_name_defaults_to_none(monkeypatch: pytest.MonkeyPatch) -> None:
    """Omitted provider_name remains unset so Vagrant can select a provider."""

    class CapturedArgumentSpec(Exception):
        pass

    def capture_argument_spec(**kwargs: Any) -> None:
        assert kwargs["argument_spec"]["provider_name"]["default"] is None
        raise CapturedArgumentSpec

    monkeypatch.setattr(vagrant_module, "AnsibleModule", capture_argument_spec)

    with pytest.raises(CapturedArgumentSpec):
        vagrant_module.main()


def test_up_passes_explicit_provider_even_if_default_env_is_set(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Explicit provider selection must override VAGRANT_DEFAULT_PROVIDER."""
    monkeypatch.setenv("VAGRANT_DEFAULT_PROVIDER", "virtualbox")
    client = make_up_client("libvirt", monkeypatch)

    with pytest.raises(AnsibleExitJson):
        client.up()

    client._vagrant.up.assert_called_once_with(  # pylint: disable=protected-access
        provider="libvirt",
        provision=False,
    )


def test_up_omits_provider_when_not_configured(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    """Let Vagrant choose the provider when provider_name is omitted."""
    client = make_up_client(None, monkeypatch)

    with pytest.raises(AnsibleExitJson):
        client.up()

    client._vagrant.up.assert_called_once_with(  # pylint: disable=protected-access
        provision=False,
    )


def test_vagrantfile_omits_provider_block_when_not_configured() -> None:
    """Avoid pinning a provider in the Vagrantfile when none was selected."""
    # pylint: disable=protected-access
    config = make_client(
        provider_name=None
    )._get_instance_vagrant_config_dict(  # pylint: disable=protected-access
        {"name": "instance"},
    )

    rendered = render_vagrantfile([config])

    assert 'c.vm.provider "None"' not in rendered
    assert 'c.vm.provider "virtualbox"' not in rendered


def test_vagrantfile_keeps_explicit_provider_configuration() -> None:
    """Keep provider-specific configuration when the user selects a provider."""
    # pylint: disable=protected-access
    client = make_client()
    getattr(client, "_module").params["provider_name"] = "libvirt"
    config = client._get_instance_vagrant_config_dict(
        {"name": "instance"}
    )  # pylint: disable=protected-access

    rendered = render_vagrantfile([config])

    assert 'c.vm.provider "libvirt"' in rendered
