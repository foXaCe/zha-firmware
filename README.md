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
