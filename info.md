# ZHA Firmware OTA Manager

Extends **ZHA**'s OTA firmware update system with community sources — first and
foremost the `Koenkk/zigbee-OTA` index from Zigbee2MQTT — so that Zigbee devices
missing from ZHA's default OTA providers (IKEA, Inovelli, Ledvance/OSRAM,
Sonoff, ThirdReality) can be updated.

Sources are injected **at runtime** into the zigbee/zigpy OTA registry: no
`configuration.yaml` editing, no restart.

> ⚠️ A firmware update can, in rare cases, break a feature or brick a device.
> Use with care.

## Configuration

Settings → Devices & Services → Add Integration → "ZHA Firmware OTA Manager".
