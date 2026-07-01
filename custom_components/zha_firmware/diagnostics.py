"""Diagnostics for the ZHA Firmware OTA Manager integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

    from . import ZhaFirmwareConfigEntry


async def async_get_config_entry_diagnostics(
    hass: HomeAssistant, entry: ZhaFirmwareConfigEntry
) -> dict[str, Any]:
    """Return diagnostics for a config entry."""
    coordinator = entry.runtime_data
    return {
        "options": dict(entry.options),
        "status": coordinator.data,
        "last_update_success": coordinator.last_update_success,
    }
