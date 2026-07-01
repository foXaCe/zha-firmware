# ZHA Firmware OTA Manager

Étend le système de mise à jour firmware OTA de **ZHA** avec des sources
communautaires — au premier chef l'index `Koenkk/zigbee-OTA` de Zigbee2MQTT —
afin de couvrir les appareils Zigbee absents des providers OTA par défaut de ZHA
(IKEA, Inovelli, Ledvance/OSRAM, Sonoff, ThirdReality).

Les sources sont injectées **à chaud** dans le registre OTA de zigbee/zigpy :
aucune édition de `configuration.yaml`, aucun redémarrage.

> ⚠️ Une mise à jour firmware peut, dans de rares cas, casser une fonction ou
> rendre un appareil inutilisable. À utiliser en connaissance de cause.

## Configuration

Paramètres → Appareils et services → Ajouter une intégration → « ZHA Firmware OTA Manager ».
