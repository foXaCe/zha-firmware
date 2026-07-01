# ZHA Firmware OTA Manager

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![CI][ci-shield]][ci]
[![hassfest][hassfest-shield]][hassfest]
[![Maintenance][maintenance-shield]][maintenance]

_Extend ZHA's OTA firmware update system with community sources._

ZHA can already perform OTA firmware updates, but its default providers are
limited to a handful of manufacturers (IKEA, Inovelli, Ledvance/OSRAM, Sonoff,
ThirdReality). For every other device the `update` entity stays `Unknown`. This
integration adds **extra OTA sources** — first and foremost the
[`Koenkk/zigbee-OTA`][koenkk] index used by Zigbee2MQTT, which covers hundreds
of devices — by **injecting them at runtime** into the zigbee/zigpy OTA
registry. No `configuration.yaml` editing, no restart.

> [!WARNING]
> A firmware update can break a feature (e.g. group binding on some devices)
> or, in rare cases, brick a device. Use this integration at your own risk.

## Features

- Adds reliable community OTA sources to ZHA: **Koenkk/zigbee-OTA** (Zigbee2MQTT)
  and the official **zigpy-ota** index — both enabled by default.
- **Runtime** injection of OTA providers (no YAML, no restart), kept alive
  across ZHA reloads.
- A UI (options) to manage sources: toggle Koenkk / zigpy, add extra remote
  index URLs, add a local firmware folder.
- A **status sensor** (number of active sources, ZHA reachability) and
  downloadable **diagnostics**.
- A `zha_firmware.check_updates` service to re-register the sources and ask
  devices to re-check for firmware.
- _(planned)_ a local firmware mirror/cache (offline, GitHub rate-limit safe).

## Requirements

- Home Assistant >= 2025.1
- The **ZHA** integration configured and running

## Installation

### HACS (recommended)

1. Open HACS in Home Assistant.
2. Add this repository as a custom repository (type: Integration).
3. Search for "ZHA Firmware OTA Manager" and install it.
4. Restart Home Assistant.
5. Settings → Devices & Services → Add Integration → "ZHA Firmware OTA Manager".

### Manual

1. Copy `custom_components/zha_firmware/` into `<config>/custom_components/`.
2. Restart Home Assistant.
3. Add the integration from the UI.

## Configuration

Settings → Devices & Services → Add Integration → "ZHA Firmware OTA Manager".

## How it works

The integration retrieves the zigpy application object exposed by ZHA
(`gateway_proxy.application`) and registers additional OTA providers via
`application.ota.register_provider(...)`. An OTA refresh
(`ota.broadcast_notify()`) then asks devices to re-check for available firmware,
which populates ZHA's `update.*` entities.

## Troubleshooting

**A device's update entity shows "Unknown".** No firmware image exists for it
in any active source. This is common for white-label Tuya devices
(`_TZ3000_…`): no manufacturer publishes their firmware, so there is nothing to
offer — Zigbee2MQTT shows the same.

**No update is offered even though the device is known.** Most likely the
installed firmware is already the same as (or newer than) what the indexes
contain. The `update` entity's `installed_version` / `latest_version`
attributes tell you exactly what was matched.

**Battery-powered devices never show a version.** Sleeping devices only check
for firmware when they wake up. Call the `zha_firmware.check_updates` service,
then wake the device (press a button, rotate a cube…) and give it a minute.

**"ZHA gateway unreachable" repair issue.** The integration could not reach
ZHA's runtime for several minutes. Check that ZHA is loaded and running
(Settings → Devices & Services → ZHA). The integration retries automatically
and the issue clears itself once ZHA is back.

**Check the integration status at a glance.** The diagnostic sensor
**Active OTA sources** shows how many sources are registered; its attributes
list each source URL, the number of firmware entries it serves, and the last
injection time.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[MIT](LICENSE)

<!-- Badges -->
[releases-shield]: https://img.shields.io/github/release/foXaCe/zha-firmware.svg?style=for-the-badge
[releases]: https://github.com/foXaCe/zha-firmware/releases
[license-shield]: https://img.shields.io/github/license/foXaCe/zha-firmware.svg?style=for-the-badge
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[ci-shield]: https://img.shields.io/github/actions/workflow/status/foXaCe/zha-firmware/ci.yml?branch=main&style=for-the-badge&label=CI
[ci]: https://github.com/foXaCe/zha-firmware/actions/workflows/ci.yml
[hassfest-shield]: https://img.shields.io/github/actions/workflow/status/foXaCe/zha-firmware/hassfest.yml?branch=main&style=for-the-badge&label=hassfest
[hassfest]: https://github.com/foXaCe/zha-firmware/actions/workflows/hassfest.yml
[maintenance-shield]: https://img.shields.io/maintenance/yes/2026.svg?style=for-the-badge
[maintenance]: https://github.com/foXaCe/zha-firmware
[koenkk]: https://github.com/Koenkk/zigbee-OTA
