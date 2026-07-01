# ZHA Firmware OTA Manager

[![GitHub Release][releases-shield]][releases]
[![License][license-shield]](LICENSE)
[![hacs][hacsbadge]][hacs]
[![CI][ci-shield]][ci]
[![hassfest][hassfest-shield]][hassfest]
[![Maintenance][maintenance-shield]][maintenance]

_Étend le système de mise à jour firmware OTA de **ZHA** avec des sources communautaires._

ZHA sait déjà faire des mises à jour firmware OTA, mais ses providers par défaut se
limitent à une poignée de fabricants (IKEA, Inovelli, Ledvance/OSRAM, Sonoff,
ThirdReality). Pour tous les autres appareils, l'entité `update` reste à
`Unknown`. Cette intégration ajoute des **sources OTA supplémentaires** — au
premier chef l'index [`Koenkk/zigbee-OTA`][koenkk] de Zigbee2MQTT, qui couvre des
centaines d'appareils — en les **injectant à chaud** dans le registre OTA de
zigbee/zigpy. Aucune édition de `configuration.yaml`, aucun redémarrage.

> [!WARNING]
> Une mise à jour firmware peut casser une fonction (ex. le group binding sur
> certains appareils) ou, dans de rares cas, rendre un appareil inutilisable.
> Utilisez cette intégration en connaissance de cause.

## Fonctionnalités

- Ajoute la source communautaire **Zigbee2MQTT** (`Koenkk/zigbee-OTA`) à ZHA
- Injection **à chaud** des providers OTA (pas de YAML, pas de redémarrage)
- _(à venir)_ interface de gestion des sources OTA
- _(à venir)_ miroir/cache local des firmwares (offline, anti rate-limit GitHub)

> **État** : bootstrap en cours — le squelette se charge dans Home Assistant ;
> la logique d'injection arrive dans une passe ultérieure.

## Prérequis

- Home Assistant ≥ 2025.1
- L'intégration **ZHA** configurée et active

## Installation

### HACS (recommandé)

1. Ouvrez HACS dans Home Assistant.
2. Ajoutez ce dépôt comme dépôt personnalisé (type : Integration).
3. Recherchez « ZHA Firmware OTA Manager » et installez.
4. Redémarrez Home Assistant.
5. Paramètres → Appareils et services → Ajouter une intégration → « ZHA Firmware OTA Manager ».

### Manuelle

1. Copiez `custom_components/zha_firmware/` dans `<config>/custom_components/`.
2. Redémarrez Home Assistant.
3. Ajoutez l'intégration depuis l'interface.

## Configuration

Paramètres → Appareils et services → Ajouter une intégration → « ZHA Firmware OTA Manager ».

## Fonctionnement

L'intégration récupère l'objet application zigpy exposé par ZHA
(`gateway_proxy.application`) et enregistre des providers OTA supplémentaires via
`application.ota.register_provider(...)`. Un rafraîchissement OTA
(`ota.broadcast_notify()`) invite ensuite les appareils à re-vérifier la
disponibilité d'un firmware, ce qui peuple les entités `update.*` de ZHA.

## Contribuer

Voir [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

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
