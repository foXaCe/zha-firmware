"""Coordinator that injects OTA sources into ZHA and exposes their status."""

from __future__ import annotations

import asyncio
import logging
from typing import TYPE_CHECKING, Any

from homeassistant.helpers import issue_registry as ir
from homeassistant.helpers.aiohttp_client import async_get_clientsession
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator
from homeassistant.util import dt as dt_util

from .const import (
    CONF_BROADCAST,
    DEFAULT_BROADCAST,
    DOMAIN,
    ENSURE_INTERVAL,
    INDEX_FETCH_TIMEOUT,
    ISSUE_ZHA_UNREACHABLE,
    UNREACHABLE_FAILURES_BEFORE_ISSUE,
)
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
    ``coordinator.data`` for the status sensor and diagnostics. When the
    gateway stays unreachable, a repair issue is raised in the UI.
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
        self._consecutive_failures = 0

    async def async_force(self) -> None:
        """Force re-registration and an OTA re-check (used by the service)."""
        self._last_app = None
        await self.async_request_refresh()

    async def _async_update_data(self) -> StatusData:
        """Ensure our sources are registered and return the current status."""
        specs = build_provider_specs(self.entry.options)
        sources = [target for _kind, target in specs]
        previous = self.data or {}
        last_injection = previous.get("last_injection")
        source_stats = previous.get("source_stats")

        app = get_zigpy_app(self.hass)
        if app is None:
            self._last_app = None
            self._consecutive_failures += 1
            if not self._warned_unreachable:
                _LOGGER.warning(
                    "Could not reach the ZHA gateway; OTA sources not injected "
                    "(will keep retrying)"
                )
                self._warned_unreachable = True
            else:
                _LOGGER.debug("ZHA gateway still not reachable")
            if self._consecutive_failures >= UNREACHABLE_FAILURES_BEFORE_ISSUE:
                ir.async_create_issue(
                    self.hass,
                    DOMAIN,
                    ISSUE_ZHA_UNREACHABLE,
                    is_fixable=False,
                    severity=ir.IssueSeverity.WARNING,
                    translation_key=ISSUE_ZHA_UNREACHABLE,
                    learn_more_url="https://github.com/foXaCe/zha-firmware#troubleshooting",
                )
            return {
                "status": "gateway_unreachable",
                "reachable": False,
                "source_count": len(specs),
                "sources": sources,
                "source_stats": source_stats,
                "last_injection": last_injection,
            }

        self._warned_unreachable = False
        self._consecutive_failures = 0
        ir.async_delete_issue(self.hass, DOMAIN, ISSUE_ZHA_UNREACHABLE)

        if app is not self._last_app:
            providers = instantiate_providers(specs)
            for provider in providers:
                app.ota.register_provider(provider)
            self._last_app = app
            last_injection = dt_util.utcnow().isoformat()
            _LOGGER.info("Registered %d OTA source(s) with ZHA", len(providers))
            if self.entry.options.get(CONF_BROADCAST, DEFAULT_BROADCAST):
                await async_broadcast_notify(app)
            source_stats = await self._async_fetch_source_stats(specs)

        return {
            "status": "ok",
            "reachable": True,
            "source_count": len(specs),
            "sources": sources,
            "source_stats": source_stats,
            "last_injection": last_injection,
        }

    async def _async_fetch_source_stats(
        self, specs: list[tuple[str, str]]
    ) -> dict[str, int | None]:
        """Fetch each remote index and count its firmware entries (best effort)."""
        urls = [target for kind, target in specs if kind == "z2m"]
        counts = await asyncio.gather(*(self._async_index_count(u) for u in urls))
        return dict(zip(urls, counts, strict=True))

    async def _async_index_count(self, url: str) -> int | None:
        """Return the number of firmware entries in a remote index, or None."""
        session = async_get_clientsession(self.hass)
        try:
            async with asyncio.timeout(INDEX_FETCH_TIMEOUT):
                response = await session.get(url)
                response.raise_for_status()
                # raw.githubusercontent.com serves JSON as text/plain.
                data = await response.json(content_type=None)
        except Exception:  # network/parse errors must not break the update
            _LOGGER.debug("Could not fetch index stats from %s", url, exc_info=True)
            return None
        return len(data) if isinstance(data, list) else None
