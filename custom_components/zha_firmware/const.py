"""Constants for the ZHA Firmware OTA Manager integration."""

from __future__ import annotations

from typing import Final

DOMAIN: Final = "zha_firmware"
INTEGRATION_NAME: Final = "ZHA Firmware OTA Manager"

# The integration whose OTA system we extend. Declared in ``after_dependencies``
# so we are set up after it when it is present.
ZHA_DOMAIN: Final = "zha"

# Community OTA source from Zigbee2MQTT (Koenkk/zigbee-OTA). This is the same
# index Z2M uses; it covers hundreds of devices missing from ZHA's default OTA
# providers. It is injected at runtime into the zigbee/zigpy OTA registry.
Z2M_KOENKK_INDEX_URL: Final = (
    "https://raw.githubusercontent.com/Koenkk/zigbee-OTA/master/index.json"
)

# Service that (re-)registers the OTA sources and asks devices to re-check.
SERVICE_CHECK_UPDATES: Final = "check_updates"
