"""Select platform for Atmoce Battery."""
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback

from .const import DOMAIN
from .controls import (
    AtmoceForcedCommandSelect,
    AtmoceForcedModeSelect,
    AtmoceWorkModeSelect,
)
from .coordinator import AtmoceCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities: AddEntitiesCallback
) -> None:
    coordinator: AtmoceCoordinator = hass.data[DOMAIN][entry.entry_id]
    if not coordinator.has_battery:
        async_add_entities([])
        return

    async_add_entities([
        AtmoceForcedCommandSelect(coordinator),
        AtmoceForcedModeSelect(coordinator),
        # What the battery does on its own (needs the atmocecloud.com login)
        AtmoceWorkModeSelect(coordinator),
    ])
