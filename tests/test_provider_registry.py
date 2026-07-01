"""Unit tests for the defensive ZHA gateway accessor (no HA runtime needed)."""

from __future__ import annotations

from types import SimpleNamespace

from custom_components.zha_firmware.provider_registry import get_zigpy_app


def test_get_zigpy_app_returns_none_without_zha() -> None:
    """When ZHA has no data registered, the accessor returns None."""
    fake_hass = SimpleNamespace(data={})
    assert get_zigpy_app(fake_hass) is None  # type: ignore[arg-type]


def test_get_zigpy_app_returns_none_without_gateway() -> None:
    """When ZHA data exists but the gateway proxy is missing, return None."""
    from homeassistant.components.zha.const import DATA_ZHA

    fake_hass = SimpleNamespace(data={DATA_ZHA: SimpleNamespace(gateway_proxy=None)})
    assert get_zigpy_app(fake_hass) is None  # type: ignore[arg-type]


def test_get_zigpy_app_returns_application() -> None:
    """When the gateway proxy exposes an application, it is returned."""
    from homeassistant.components.zha.const import DATA_ZHA

    sentinel = object()
    fake_hass = SimpleNamespace(
        data={
            DATA_ZHA: SimpleNamespace(
                gateway_proxy=SimpleNamespace(application=sentinel)
            )
        }
    )
    assert get_zigpy_app(fake_hass) is sentinel  # type: ignore[arg-type]
