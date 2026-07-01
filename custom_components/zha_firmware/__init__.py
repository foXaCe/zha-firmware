"""The ZHA Firmware OTA Manager integration.

Phase 1: inject configured OTA sources (Koenkk/zigbee-OTA and any user sources)
into ZHA's running zigpy application, keep them alive across ZHA reloads via a
periodic ensure loop, and expose a service to re-run the injection on demand.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.event import async_track_time_interval
from homeassistant.helpers.start import async_at_started

from .const import DOMAIN, ENSURE_INTERVAL, SERVICE_CHECK_UPDATES
from .provider_registry import OtaSourceManager

if TYPE_CHECKING:
    from datetime import datetime

    from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

# No entity platforms yet: this integration only injects OTA sources into ZHA.
PLATFORMS: list[str] = []

type ZhaFirmwareConfigEntry = ConfigEntry[OtaSourceManager]


async def async_setup_entry(hass: HomeAssistant, entry: ZhaFirmwareConfigEntry) -> bool:
    """Set up ZHA Firmware OTA Manager from a config entry."""
    manager = OtaSourceManager(hass, entry)
    entry.runtime_data = manager

    async def _on_started(_hass: HomeAssistant) -> None:
        await manager.async_ensure()

    async def _periodic(_now: datetime) -> None:
        await manager.async_ensure()

    # Initial injection once HA (hence ZHA) has started; runs immediately if HA
    # is already started when the entry is set up.
    entry.async_on_unload(async_at_started(hass, _on_started))
    # Idempotent re-injection loop: re-registers our sources after a ZHA reload.
    entry.async_on_unload(async_track_time_interval(hass, _periodic, ENSURE_INTERVAL))
    # Rebuild sources when the user changes options.
    entry.async_on_unload(entry.add_update_listener(_async_reload_on_update))

    async def _handle_check_updates(_call: ServiceCall) -> None:
        await manager.async_ensure(force=True)

    hass.services.async_register(DOMAIN, SERVICE_CHECK_UPDATES, _handle_check_updates)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ZhaFirmwareConfigEntry
) -> bool:
    """Unload a config entry."""
    hass.services.async_remove(DOMAIN, SERVICE_CHECK_UPDATES)
    return True


async def _async_reload_on_update(
    hass: HomeAssistant, entry: ZhaFirmwareConfigEntry
) -> None:
    """Reload the entry when its options change so sources are rebuilt."""
    await hass.config_entries.async_reload(entry.entry_id)
