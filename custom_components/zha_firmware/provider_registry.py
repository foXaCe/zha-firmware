"""Inject extra OTA providers into ZHA's running zigpy application.

This is the core of the integration: it reaches the zigpy
``ControllerApplication`` exposed by ZHA and registers additional OTA providers
(the community Koenkk/zigbee-OTA index and any user-configured sources), then
asks devices to re-check for firmware so ZHA's ``update.*`` entities populate.
"""

from __future__ import annotations

import logging
import pathlib
from typing import TYPE_CHECKING, Any

from .const import (
    CONF_BROADCAST,
    CONF_EXTRA_URLS,
    CONF_LOCAL_FOLDER,
    CONF_USE_KOENKK,
    CONF_USE_ZIGPY,
    DEFAULT_BROADCAST,
    DEFAULT_USE_KOENKK,
    DEFAULT_USE_ZIGPY,
    Z2M_KOENKK_INDEX_URL,
    ZIGPY_OTA_INDEX_URL,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from homeassistant.config_entries import ConfigEntry
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

# A provider spec is a (kind, target) pair, kept plain so it is easy to build
# and unit test without importing zigpy. ``kind`` is "z2m" (remote index URL) or
# "advanced" (local firmware folder).
type ProviderSpec = tuple[str, str]


def _gateway_from_data(zha_data: Any) -> Any:
    """Reach the ZHA (zha-lib) Gateway object from ZHA's data (import-free).

    Kept free of ZHA imports so it can be unit tested without the ``zha``
    package installed.
    """
    gateway_proxy = getattr(zha_data, "gateway_proxy", None)
    return getattr(gateway_proxy, "gateway", None)


def _app_from_gateway(gateway: Any) -> Any:
    """Return the zigpy ``ControllerApplication`` (has ``.ota``) from a gateway."""
    if gateway is None:
        return None
    return getattr(gateway, "application_controller", None) or getattr(
        gateway, "application", None
    )


def _official_gateway(hass: HomeAssistant) -> Any:
    """Return ZHA's Gateway via its official helper, or ``None`` if unavailable."""
    try:
        from homeassistant.components.zha.helpers import get_zha_gateway
    except ImportError:
        return None
    try:
        return get_zha_gateway(hass)
    except Exception:  # ZHA not set up yet (raises ValueError) or layout changed
        return None


def get_zigpy_app(hass: HomeAssistant) -> Any:
    """Return the running zigpy ``ControllerApplication`` exposed by ZHA, or None.

    Prefers ZHA's official helper (``get_zha_gateway``) and reads
    ``gateway.application_controller``; falls back to reaching into
    ``hass.data`` defensively. These are private, version-dependent ZHA APIs.
    """
    gateway = _official_gateway(hass)
    if gateway is None:
        try:
            from homeassistant.components.zha.const import DATA_ZHA
        except ImportError:
            _LOGGER.debug("ZHA is not available")
            return None
        gateway = _gateway_from_data(hass.data.get(DATA_ZHA))

    app = _app_from_gateway(gateway)
    if app is None and gateway is not None:
        _LOGGER.debug(
            "ZHA gateway found but no application controller; type=%s attrs=%s",
            type(gateway).__name__,
            [a for a in dir(gateway) if not a.startswith("_")],
        )
    return app


def build_provider_specs(options: Mapping[str, Any]) -> list[ProviderSpec]:
    """Turn the config-entry options into a list of provider specs (pure)."""
    specs: list[ProviderSpec] = []

    if options.get(CONF_USE_KOENKK, DEFAULT_USE_KOENKK):
        specs.append(("z2m", Z2M_KOENKK_INDEX_URL))

    if options.get(CONF_USE_ZIGPY, DEFAULT_USE_ZIGPY):
        specs.append(("z2m", ZIGPY_OTA_INDEX_URL))

    raw_urls = options.get(CONF_EXTRA_URLS) or ""
    lines = raw_urls.splitlines() if isinstance(raw_urls, str) else raw_urls
    for line in lines:
        url = str(line).strip()
        if url:
            specs.append(("z2m", url))

    folder = str(options.get(CONF_LOCAL_FOLDER) or "").strip()
    if folder:
        specs.append(("advanced", folder))

    return specs


def _instantiate_providers(specs: list[ProviderSpec]) -> list[Any]:
    """Build zigpy provider objects from specs (needs the zigpy package)."""
    try:
        from zigpy.ota import providers
    except ImportError:
        _LOGGER.error("zigpy is unavailable; cannot build OTA providers")
        return []

    built: list[Any] = []
    for kind, target in specs:
        if kind == "z2m":
            built.append(providers.RemoteZ2MProvider(target))
        elif kind == "advanced":
            built.append(providers.AdvancedFileProvider(pathlib.Path(target)))
    return built


class OtaSourceManager:
    """Own the injection of OTA sources into ZHA and keep them alive.

    ``async_ensure`` is idempotent: it only (re-)registers providers when the
    ZHA application object changes (i.e. the first time, or after a ZHA reload),
    which is what a periodic ensure loop relies on.
    """

    def __init__(self, hass: HomeAssistant, entry: ConfigEntry) -> None:
        """Initialise the manager for a config entry."""
        self.hass = hass
        self.entry = entry
        self._last_app: Any = None
        self._warned_unreachable = False

    async def async_ensure(self, *, force: bool = False) -> bool:
        """Ensure our providers are registered with the current ZHA gateway.

        Returns ``True`` when ZHA is reachable, ``False`` otherwise.
        """
        app = get_zigpy_app(self.hass)
        if app is None:
            self._last_app = None
            # Warn once, then stay at debug level to avoid spamming the log while
            # the ensure loop keeps retrying (e.g. during a ZHA reload).
            if not self._warned_unreachable:
                _LOGGER.warning(
                    "Could not reach the ZHA gateway; OTA sources not injected "
                    "(will keep retrying)"
                )
                self._warned_unreachable = True
            else:
                _LOGGER.debug("ZHA gateway still not reachable")
            return False

        self._warned_unreachable = False
        if app is self._last_app and not force:
            return True

        specs = build_provider_specs(self.entry.options)
        providers = _instantiate_providers(specs)
        for provider in providers:
            app.ota.register_provider(provider)
        self._last_app = app
        _LOGGER.info("Registered %d OTA source(s) with ZHA", len(providers))

        if self.entry.options.get(CONF_BROADCAST, DEFAULT_BROADCAST):
            await self._broadcast(app)
        return True

    async def _broadcast(self, app: Any) -> None:
        """Ask devices to re-check for firmware (best effort)."""
        try:
            await app.ota.broadcast_notify()
        except Exception:  # broad on purpose: a failed broadcast must not break setup
            _LOGGER.debug("OTA broadcast_notify failed (non-fatal)", exc_info=True)
