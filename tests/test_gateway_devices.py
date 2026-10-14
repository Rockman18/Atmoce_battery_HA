"""Tests for gateway-only entity setup."""
from types import SimpleNamespace

import pytest

from custom_components.atmoce import (
    binary_sensor,
    button,
    number,
    select,
    sensor,
    switch,
)
from custom_components.atmoce.const import DOMAIN


@pytest.mark.asyncio
async def test_zero_batteries_keeps_only_gateway_entities(monkeypatch):
    coordinator = SimpleNamespace(has_battery=False)
    entry = SimpleNamespace(entry_id="entry")
    hass = SimpleNamespace(data={DOMAIN: {"entry": coordinator}})
    created: dict[str, list] = {}

    def add_entities(platform: str):
        def add(entities):
            created[platform].extend(entities)

        created[platform] = []
        return add

    monkeypatch.setattr(sensor, "AtmoceSensor", lambda _, description: description)
    monkeypatch.setattr(button, "AtmoceResetButton", lambda _: "gateway_reset")

    await sensor.async_setup_entry(hass, entry, add_entities("sensor"))
    await binary_sensor.async_setup_entry(hass, entry, add_entities("binary_sensor"))
    await switch.async_setup_entry(hass, entry, add_entities("switch"))
    await number.async_setup_entry(hass, entry, add_entities("number"))
    await select.async_setup_entry(hass, entry, add_entities("select"))
    await button.async_setup_entry(hass, entry, add_entities("button"))

    assert all(not description.is_battery for description in created["sensor"])
    assert created["binary_sensor"] == []
    assert created["switch"] == []
    assert created["number"] == []
    assert created["select"] == []
    assert created["button"] == ["gateway_reset"]
