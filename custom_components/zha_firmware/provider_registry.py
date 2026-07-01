"""Inject extra OTA providers into ZHA's running zigpy application.

This is the core of the integration: it reaches the zigpy
``ControllerApplication`` exposed by ZHA and registers additional OTA providers
(currently the community Koenkk/zigbee-OTA index), then asks devices to
re-check for firmware so ZHA's ``update.*`` entities populate.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING, Any

from .const import Z2M_KOENKK_INDEX_URL

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)


def _extract_app(zha_data: Any) -> Any:
    """Traverse ZHA's data object to reach the zigpy application, or ``None``.

    Kept import-free (no ZHA modules) so it can be unit tested without the
    ``zha`` package installed.
    """
    gateway_proxy = getattr(zha_data, "gateway_proxy", None)
    if gateway_proxy is None:
        return None
    return getattr(gateway_proxy, "application", None)


def get_zigpy_app(hass: HomeAssistant) -> Any:
    """Return the running zigpy ``ControllerApplication`` exposed by ZHA.

    Returns ``None`` when ZHA is not available or its gateway is not ready yet.

    This relies on ZHA internals
    (``hass.data[DATA_ZHA].gateway_proxy.application``) which are a private,
    version-dependent API, so every step is accessed defensively.
    """
    try:
        from homeassistant.components.zha.const import DATA_ZHA
    except ImportError:
        _LOGGER.debug("ZHA is not available")
        return None

    app = _extract_app(hass.data.get(DATA_ZHA))
    if app is None:
        _LOGGER.debug("ZHA gateway is not ready yet")
    return app


async def async_ensure_providers(hass: HomeAssistant) -> bool:
    """Register the community OTA providers into ZHA and trigger a re-check.

    Idempotent: zigpy's ``register_provider`` de-duplicates, so this can be
    called repeatedly (e.g. after a ZHA reload). Returns ``True`` on success.
    """
    app = get_zigpy_app(hass)
    if app is None:
        _LOGGER.warning("Could not reach the ZHA gateway; OTA providers not injected")
        return False

    try:
        from zigpy.ota import providers
    except ImportError:
        _LOGGER.error("zigpy is unavailable; cannot inject OTA providers")
        return False

    provider = providers.RemoteZ2MProvider(Z2M_KOENKK_INDEX_URL)
    app.ota.register_provider(provider)
    _LOGGER.info("Registered community OTA provider (Koenkk/zigbee-OTA) with ZHA")

    try:
        await app.ota.broadcast_notify()
    except Exception:
        _LOGGER.debug("OTA broadcast_notify failed (non-fatal)", exc_info=True)

    return True
