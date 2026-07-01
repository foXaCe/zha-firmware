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
    CONF_EXTRA_URLS,
    CONF_LOCAL_FOLDER,
    CONF_USE_KOENKK,
    CONF_USE_ZIGPY,
    DEFAULT_USE_KOENKK,
    DEFAULT_USE_ZIGPY,
    Z2M_KOENKK_INDEX_URL,
    ZIGPY_OTA_INDEX_URL,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

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


def invalid_urls(raw: str | list[str]) -> list[str]:
    """Return the entries of ``raw`` that are not http(s) URLs (pure)."""
    lines = raw.splitlines() if isinstance(raw, str) else raw
    bad: list[str] = []
    for line in lines:
        url = str(line).strip()
        if url and not url.lower().startswith(("http://", "https://")):
            bad.append(url)
    return bad


def validate_folder(path_str: str) -> bool:
    """Check a firmware folder path: absolute, creatable, and a directory.

    Blocking filesystem I/O — call via ``hass.async_add_executor_job``.
    """
    path = pathlib.Path(path_str)
    if not path.is_absolute():
        return False
    try:
        path.mkdir(parents=True, exist_ok=True)
    except OSError:
        return False
    return path.is_dir()


def instantiate_providers(specs: list[ProviderSpec]) -> list[Any]:
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


async def async_broadcast_notify(app: Any) -> None:
    """Ask devices to re-check for firmware (best effort)."""
    try:
        await app.ota.broadcast_notify()
    except Exception:  # broad on purpose: a failed broadcast must not break setup
        _LOGGER.debug("OTA broadcast_notify failed (non-fatal)", exc_info=True)
