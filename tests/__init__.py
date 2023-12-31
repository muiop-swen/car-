"""Tests for Porsche Connect integration."""
from __future__ import annotations

import json
from typing import Any
from unittest.mock import Mock
from unittest.mock import patch

from custom_components.porscheconnect import DOMAIN
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from pytest_homeassistant_custom_component.common import MockConfigEntry

from .const import MOCK_CONFIG

TEST_CONFIG_ENTRY_ID = "77889900ac"


def load_fixture_json(name):
    with open(f"tests/fixtures/{name}.json") as json_file:
        data = json.load(json_file)
        return data


def create_mock_porscheconnect_config_entry(
    hass: HomeAssistant,
    data: dict[str, Any] | None = None,
    options: dict[str, Any] | None = None,
) -> ConfigEntry:
    """Add a test config entry."""
    config_entry: MockConfigEntry = MockConfigEntry(
        entry_id=TEST_CONFIG_ENTRY_ID,
        domain=DOMAIN,
        data=data or MOCK_CONFIG,
        title="",
        options=options or {},
    )
    config_entry.add_to_hass(hass)
    return config_entry


async def setup_mock_porscheconnect_config_entry(
    hass: HomeAssistant,
    data: dict[str, Any] | None = None,
    config_entry: ConfigEntry | None = None,
    client: Mock | None = None,
) -> ConfigEntry:
    #    client_data = "taycan"
    #    if data is not None:
    #        client_data = data.get("client_data", "taycan")
    """Add a mock porscheconnect config entry to hass."""
    config_entry = config_entry or create_mock_porscheconnect_config_entry(hass, data)

    fixture_name = "taycan"
    fixture_data = load_fixture_json(fixture_name)
    print(f"Using mock connedion fixture {fixture_name}")

    async def mock_get(self, url, params=None):
        print(f"Mock connection GET {url}")
        print(params)
        ret = fixture_data["GET"].get(url, {})
        print(ret)
        return ret

    async def mock_post(self, url, data=None, json=None):
        print(f"POST {url}")
        print(data)
        print(json)
        return {}

    async def mock_tokens(self, application, wasExpired=False):
        print(f"Request mock token {application}")
        return {}

    with patch("pyporscheconnectapi.client.Connection.get", mock_get), patch(
        "pyporscheconnectapi.client.Connection.post", mock_post
    ), patch("pyporscheconnectapi.client.Connection._requestToken", mock_tokens):
        await hass.config_entries.async_setup(config_entry.entry_id)
        await hass.async_block_till_done()
    return config_entry
