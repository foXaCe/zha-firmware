"""The ZHA Firmware OTA Manager integration.

Squelette minimal (bootstrap). La logique métier — injection à chaud de
providers OTA dans le registre zigpy de ZHA via
``gateway_proxy.application.ota.register_provider()`` — sera ajoutée dans une
passe ultérieure.
"""

from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from homeassistant.config_entries import ConfigEntry

from .const import DOMAIN

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant

_LOGGER = logging.getLogger(__name__)

# Aucune plateforme d'entités pour l'instant : le squelette se contente de charger.
PLATFORMS: list[str] = []

type ZhaFirmwareConfigEntry = ConfigEntry


async def async_setup_entry(hass: HomeAssistant, entry: ZhaFirmwareConfigEntry) -> bool:
    """Set up ZHA Firmware OTA Manager from a config entry."""
    _LOGGER.debug(
        "Mise en place de %s (squelette — aucun provider OTA injecté pour l'instant)",
        DOMAIN,
    )
    return True


async def async_unload_entry(
    hass: HomeAssistant, entry: ZhaFirmwareConfigEntry
) -> bool:
    """Unload a config entry."""
    _LOGGER.debug("Déchargement de %s", DOMAIN)
    return True
