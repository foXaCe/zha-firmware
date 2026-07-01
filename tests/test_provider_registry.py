"""Unit tests for the pure helpers of provider_registry (no HA/zha runtime)."""

from __future__ import annotations

from types import SimpleNamespace

from custom_components.zha_firmware.const import Z2M_KOENKK_INDEX_URL
from custom_components.zha_firmware.provider_registry import (
    _extract_app,
    build_provider_specs,
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


def test_specs_default_includes_koenkk() -> None:
    """By default the Koenkk community index is included."""
    assert ("z2m", Z2M_KOENKK_INDEX_URL) in build_provider_specs({})


def test_specs_koenkk_can_be_disabled() -> None:
    """Disabling Koenkk removes it from the specs."""
    specs = build_provider_specs({"use_koenkk": False})
    assert all(target != Z2M_KOENKK_INDEX_URL for _, target in specs)


def test_specs_extra_urls_and_local_folder() -> None:
    """Extra URLs (one per line, blanks ignored) and a local folder are added."""
    specs = build_provider_specs(
        {
            "use_koenkk": False,
            "extra_urls": "https://a/index.json\n   \nhttps://b/index.json",
            "local_folder": " /config/zigbee_ota ",
        }
    )
    assert ("z2m", "https://a/index.json") in specs
    assert ("z2m", "https://b/index.json") in specs
    assert ("advanced", "/config/zigbee_ota") in specs
