"""Constants for the ZHA Firmware OTA Manager integration."""

from __future__ import annotations

from datetime import timedelta
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

# Options keys.
CONF_USE_KOENKK: Final = "use_koenkk"
CONF_EXTRA_URLS: Final = "extra_urls"
CONF_LOCAL_FOLDER: Final = "local_folder"
CONF_BROADCAST: Final = "broadcast"

DEFAULT_USE_KOENKK: Final = True
DEFAULT_BROADCAST: Final = True

# How often we re-check that our providers are still registered with ZHA.
# ZHA rebuilds its OTA provider list on every gateway (re)start, so an idempotent
# re-injection loop keeps our sources alive across ZHA reloads.
ENSURE_INTERVAL: Final = timedelta(minutes=2)

# Service that (re-)registers the OTA sources and asks devices to re-check.
SERVICE_CHECK_UPDATES: Final = "check_updates"
