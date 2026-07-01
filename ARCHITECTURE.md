# Architecture

## Goal

Extend **ZHA**'s OTA firmware update system with community sources (first and
foremost `Koenkk/zigbee-OTA` from Zigbee2MQTT), without requiring the user to
edit `configuration.yaml` or restart.

## Technical background

- ZHA can already push OTA firmware, through Home Assistant's standard
  `update.*` entities, enabled by default.
- Its default OTA providers are limited to a few manufacturers (IKEA, Inovelli,
  Ledvance/OSRAM, Sonoff, ThirdReality). Other devices stay `Unknown`.
- zigpy already exposes `z2m` / `z2m_local` / `advanced` provider types and a
  **public** `OTA.register_provider()` method — the internal provider list is a
  mutable Python list.

## Access point into ZHA

```python
from homeassistant.components.zha.const import DATA_ZHA

zigpy_app = hass.data[DATA_ZHA].gateway_proxy.application  # ControllerApplication
zigpy_app.ota.register_provider(provider)                  # public, de-duplicated
```

Provider classes (`zigpy.ota.providers`):

- `RemoteZ2MProvider(url=...)` — remote Zigbee2MQTT-style index (Koenkk).
- `LocalZ2MProvider(index_file=Path)` — local index (mirror).
- `AdvancedFileProvider(path=Path)` — local firmware folder.

After injection, `await zigpy_app.ota.broadcast_notify()` asks devices to
re-check for firmware, which populates the `update.*` entities.

## Target flow

```
config entry (UI) ──▶ provider_registry ──▶ zigpy_app.ota.register_provider(...)
                                              │
       coordinator (ensure loop) ────────────┘   (re-inject on ZHA reload)
                                              │
                          zigpy_app.ota.broadcast_notify()  ──▶  update.<device>
```

> ⚠️ `hass.data[DATA_ZHA].gateway_proxy.application` is a **private ZHA API**
> that may change across Home Assistant versions. Access must be defensive and
> version-guarded.

## Roadmap

- **Phase 1 (A)** — config flow UI + runtime provider injection + an ensure loop
  that re-injects on ZHA reload + an OTA refresh service. _(injection PoC landed;
  UI and ensure loop pending.)_
- **Phase 2 (B)** — a local firmware mirror/cache (offline, GitHub rate-limit
  safe) exposed as an additional `LocalZ2MProvider` source in the UI.
