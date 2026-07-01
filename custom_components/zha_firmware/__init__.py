"""The ZHA Firmware OTA Manager integration.

Phase 1 proof of concept: inject the community Koenkk/zigbee-OTA provider into
ZHA's running zigpy application once Home Assistant has started, and expose a
service to re-run the injection / firmware re-check on demand.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.start import async_at_started

from .const import DOMAIN, SERVICE_CHECK_UPDATES
from .provider_registry import async_ensure_providers

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant, ServiceCall

_LOGGER = logging.getLogger(__name__)

# No entity platforms yet: this PoC only injects OTA providers into ZHA.
PLATFORMS: list[str] = []

type ZhaFirmwareConfigEntry = ConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: ZhaFirmwareConfigEntry) -> bool:
    """Set up ZHA Firmware OTA Manager from a config entry."""

    async def _inject(_hass: HomeAssistant) -> None:
        await async_ensure_providers(hass)

    # Inject once Home Assistant (hence ZHA) has started; runs immediately if
    # HA is already started when the entry is set up.
    entry.async_on_unload(async_at_started(hass, _inject))

    async def _handle_check_updates(_call: ServiceCall) -> None:
        await async_ensure_providers(hass)

    hass.services.async_register(DOMAIN, SERVICE_CHECK_UPDATES, _handle_check_updates)

    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ZhaFirmwareConfigEntry
) -> bool:
    """Unload a config entry."""
    hass.services.async_remove(DOMAIN, SERVICE_CHECK_UPDATES)
    return True
