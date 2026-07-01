"""Coordinator that injects OTA sources into ZHA and exposes their status."""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import CONF_BROADCAST, DEFAULT_BROADCAST, DOMAIN, ENSURE_INTERVAL
from .provider_registry import (
    async_broadcast_notify,
    build_provider_specs,
    get_zigpy_app,
    instantiate_providers,
)

if TYPE_CHECKING:
    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

type StatusData = dict[str, Any]


class ZhaFirmwareCoordinator(DataUpdateCoordinator[StatusData]):
    """Register our OTA sources with ZHA and keep them alive.

    Idempotent: providers are only (re-)registered when the ZHA application
    object changes (first run, or after a ZHA reload). The result is exposed as
    ``coordinator.data`` for the status sensor and diagnostics.
    """

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Set up the coordinator for a config entry."""
        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=ENSURE_INTERVAL,
            config_entry=entry,
        )
        self.entry = entry
        self._last_app: Any = None
        self._warned_unreachable = False

    async def async_force(self) -> None:
        """Force re-registration and an OTA re-check (used by the service)."""
        self._last_app = None
        await self.async_request_refresh()

    async def _async_update_data(self) -> StatusData:
        """Ensure our sources are registered and return the current status."""
        specs = build_provider_specs(self.entry.options)
        sources = [target for _kind, target in specs]
        last_injection = self.data.get("last_injection") if self.data else None

        app = get_zigpy_app(self.hass)
        if app is None:
            self._last_app = None
            if not self._warned_unreachable:
                _LOGGER.warning(
                    "Could not reach the ZHA gateway; OTA sources not injected "
                    "(will keep retrying)"
                )
                self._warned_unreachable = True
            else:
                _LOGGER.debug("ZHA gateway still not reachable")
            return {
                "status": "gateway_unreachable",
                "reachable": False,
                "source_count": len(specs),
                "sources": sources,
                "last_injection": last_injection,
            }

        self._warned_unreachable = False
        if app is not self._last_app:
            providers = instantiate_providers(specs)
            for provider in providers:
                app.ota.register_provider(provider)
            self._last_app = app
            last_injection = dt_util.utcnow().isoformat()
            _LOGGER.info("Registered %d OTA source(s) with ZHA", len(providers))
            if self.entry.options.get(CONF_BROADCAST, DEFAULT_BROADCAST):
                await async_broadcast_notify(app)

        return {
            "status": "ok",
            "reachable": True,
            "source_count": len(specs),
            "sources": sources,
            "last_injection": last_injection,
        }
