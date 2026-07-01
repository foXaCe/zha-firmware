# Architecture

## Objectif

Étendre le système de mise à jour firmware OTA de **ZHA** avec des sources
communautaires (au premier chef `Koenkk/zigbee-OTA` de Zigbee2MQTT), sans
demander à l'utilisateur d'éditer `configuration.yaml` ni de redémarrer.

## Constat technique

- ZHA sait déjà pousser des firmwares OTA, via les entités `update.*` standard de
  Home Assistant, activées par défaut.
- Ses providers OTA par défaut se limitent à quelques fabricants (IKEA, Inovelli,
  Ledvance/OSRAM, Sonoff, ThirdReality). Les autres appareils restent à `Unknown`.
- zigpy expose déjà des types de providers `z2m` / `z2m_local` / `advanced` et une
  méthode **publique** `OTA.register_provider()` — la liste interne des providers
  est une liste Python mutable à chaud.

## Point d'accès à ZHA

```python
from homeassistant.components.zha.const import DATA_ZHA

zigpy_app = hass.data[DATA_ZHA].gateway_proxy.application  # ControllerApplication
zigpy_app.ota.register_provider(provider)                  # méthode publique, dédup incluse
```

Classes de providers (`zigpy.ota.providers`) :

- `RemoteZ2MProvider(url=...)` — index distant façon Zigbee2MQTT (Koenkk).
- `LocalZ2MProvider(index_file=Path)` — index local (miroir).
- `AdvancedFileProvider(path=Path)` — dossier de firmwares locaux.

Après injection, un `await zigpy_app.ota.broadcast_notify()` invite les appareils
à re-vérifier la disponibilité d'un firmware, ce qui peuple les entités `update.*`.

## Flux cible

```
config entry (UI) ──▶ provider_registry ──▶ zigpy_app.ota.register_provider(...)
                                              │
       coordinator (ensure-loop) ────────────┘   (ré-injection au reload de ZHA)
                                              │
                          zigpy_app.ota.broadcast_notify()  ──▶  update.<device>
```

> ⚠️ `hass.data[DATA_ZHA].gateway_proxy.application` est une **API privée de ZHA**
> susceptible de bouger selon les versions de Home Assistant. L'accès doit être
> défensif et gardé par version.

## Feuille de route

- **Phase 1 (A)** — config flow UI + injection runtime des providers + ensure-loop
  de ré-injection au reload de ZHA + service de rafraîchissement OTA.
- **Phase 2 (B)** — miroir/cache local des firmwares (offline, anti rate-limit
  GitHub) exposé comme une source `LocalZ2MProvider` supplémentaire dans l'UI.
