"""Diagnostic sensor exposing the ZHA Firmware OTA Manager status."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.components.sensor import SensorEntity
from homeassistant.const import EntityCategory
from homeassistant.helpers.device_registry import DeviceEntryType, DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN, INTEGRATION_NAME

if TYPE_CHECKING:
    from homeassistant.core import HomeAssistant
    from homeassistant.helpers.entity_platform import AddConfigEntryEntitiesCallback

    from . import ZhaFirmwareConfigEntry
    from .coordinator import ZhaFirmwareCoordinator


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ZhaFirmwareConfigEntry,
    async_add_entities: AddConfigEntryEntitiesCallback,
) -> None:
    """Set up the status sensor."""
    async_add_entities([ZhaFirmwareStatusSensor(entry.runtime_data)])


class ZhaFirmwareStatusSensor(
    CoordinatorEntity["ZhaFirmwareCoordinator"], SensorEntity
):
    """Number of OTA sources this integration has active in ZHA."""

    _attr_has_entity_name = True
    _attr_translation_key = "ota_sources"
    _attr_entity_category = EntityCategory.DIAGNOSTIC
    _attr_native_unit_of_measurement = "sources"
    _attr_icon = "mdi:package-up"

    def __init__(self, coordinator: ZhaFirmwareCoordinator) -> None:
        """Initialise the sensor."""
        super().__init__(coordinator)
        self._attr_unique_id = f"{coordinator.entry.entry_id}_ota_sources"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, coordinator.entry.entry_id)},
            name=INTEGRATION_NAME,
            entry_type=DeviceEntryType.SERVICE,
        )

    @property
    def native_value(self) -> int | None:
        """Return the number of active OTA sources."""
        data = self.coordinator.data
        if not data:
            return None
        count = data.get("source_count")
        return count if isinstance(count, int) else None

    @property
    def extra_state_attributes(self) -> dict[str, Any]:
        """Return status details."""
        data = self.coordinator.data or {}
        return {
            "status": data.get("status"),
            "zha_reachable": data.get("reachable"),
            "sources": data.get("sources"),
            "last_injection": data.get("last_injection"),
        }
