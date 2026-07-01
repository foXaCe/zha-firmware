"""The ZHA Firmware OTA Manager integration.

Injects configured OTA sources (Koenkk/zigbee-OTA, zigpy-ota and any user
sources) into ZHA's running zigpy application, keeps them alive across ZHA
reloads via a coordinator, exposes a status sensor + diagnostics, and offers a
service to re-run the injection on demand.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import Platform
from homeassistant.helpers.start import async_at_started

from .const import DOMAIN, SERVICE_CHECK_UPDATES
from .coordinator import ZhaFirmwareCoordinator

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

PLATFORMS: list[Platform] = [Platform.SENSOR]

type ZhaFirmwareConfigEntry = ConfigEntry[ZhaFirmwareCoordinator]


async def async_setup_entry(hass: HomeAssistant, entry: ZhaFirmwareConfigEntry) -> bool:
    """Set up ZHA Firmware OTA Manager from a config entry."""
    coordinator = ZhaFirmwareCoordinator(hass, entry)
    entry.runtime_data = coordinator
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    async def _on_started(_hass: HomeAssistant) -> None:
        # Once HA (hence ZHA) has fully started, prompt an immediate refresh so
        # injection happens without waiting for the periodic interval.
        await coordinator.async_request_refresh()

    entry.async_on_unload(async_at_started(hass, _on_started))
    entry.async_on_unload(entry.add_update_listener(_async_reload_on_update))

    async def _handle_check_updates(_call: ServiceCall) -> None:
        await coordinator.async_force()

    hass.services.async_register(DOMAIN, SERVICE_CHECK_UPDATES, _handle_check_updates)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ZhaFirmwareConfigEntry
) -> bool:
    """Unload a config entry."""
    hass.services.async_remove(DOMAIN, SERVICE_CHECK_UPDATES)
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


async def _async_reload_on_update(
    hass: HomeAssistant, entry: ZhaFirmwareConfigEntry
) -> None:
    """Reload the entry when its options change so sources are rebuilt."""
    await hass.config_entries.async_reload(entry.entry_id)
