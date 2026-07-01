"""Unit tests for the defensive ZHA gateway accessor (no HA/zha runtime needed)."""

from __future__ import annotations

from types import SimpleNamespace

from custom_components.zha_firmware.provider_registry import (
    _extract_app,
    get_zigpy_app,
)


def test_extract_app_none_data() -> None:
    """No ZHA data at all yields None."""
    assert _extract_app(None) is None


def test_extract_app_no_gateway() -> None:
    """ZHA data present but the gateway proxy is missing yields None."""
    assert _extract_app(SimpleNamespace(gateway_proxy=None)) is None


def test_extract_app_returns_application() -> None:
    """A gateway proxy exposing an application returns it."""
    sentinel = object()
    zha_data = SimpleNamespace(gateway_proxy=SimpleNamespace(application=sentinel))
    assert _extract_app(zha_data) is sentinel


def test_get_zigpy_app_none_when_unavailable() -> None:
    """With empty hass data (and zha not set up), the accessor returns None."""
    fake_hass = SimpleNamespace(data={})
    assert get_zigpy_app(fake_hass) is None  # type: ignore[arg-type]
