"""Constants for the ZHA Firmware OTA Manager integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "zha_firmware"
INTEGRATION_NAME: Final = "ZHA Firmware OTA Manager"

# Intégration dont on étend le système OTA. On l'écoute via `after_dependencies`
# dans le manifest afin d'être chargé après elle lorsqu'elle est présente.
ZHA_DOMAIN: Final = "zha"

# Source OTA communautaire de Zigbee2MQTT (Koenkk/zigbee-OTA). C'est le même index
# que Z2M utilise : il couvre des centaines d'appareils absents des providers OTA
# par défaut de ZHA. Sera injecté à chaud dans le registre OTA de zigpy (Phase 1).
Z2M_KOENKK_INDEX_URL: Final = (
    "https://raw.githubusercontent.com/Koenkk/zigbee-OTA/master/index.json"
)
