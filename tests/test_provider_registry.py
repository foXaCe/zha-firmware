"""Unit tests for the pure helpers of provider_registry (no HA/zha runtime)."""

from __future__ import annotations

from types import SimpleNamespace

from custom_components.zha_firmware.const import (
    Z2M_KOENKK_INDEX_URL,
    ZIGPY_OTA_INDEX_URL,
)
from custom_components.zha_firmware.provider_registry import (
    _app_from_gateway,
    _gateway_from_data,
    build_provider_specs,
    get_zigpy_app,
    invalid_urls,
    validate_folder,
)


def test_gateway_from_data_none() -> None:
    """No ZHA data at all yields None."""
    assert _gateway_from_data(None) is None


def test_gateway_from_data_no_proxy() -> None:
    """ZHA data present but no gateway proxy yields None."""
    assert _gateway_from_data(SimpleNamespace(gateway_proxy=None)) is None


def test_gateway_from_data_returns_gateway() -> None:
    """The proxy's `.gateway` is returned."""
    gateway = object()
    zha_data = SimpleNamespace(gateway_proxy=SimpleNamespace(gateway=gateway))
    assert _gateway_from_data(zha_data) is gateway


def test_app_from_gateway_none() -> None:
    """No gateway yields None."""
    assert _app_from_gateway(None) is None


def test_app_from_gateway_application_controller() -> None:
    """The zigpy app is read from `application_controller`."""
    app = object()
    assert _app_from_gateway(SimpleNamespace(application_controller=app)) is app


def test_app_from_gateway_fallback_application() -> None:
    """Falls back to `.application` when there is no `application_controller`."""
    app = object()
    assert _app_from_gateway(SimpleNamespace(application=app)) is app


def test_get_zigpy_app_none_when_unavailable() -> None:
    """With empty hass data (and zha not set up), the accessor returns None."""
    fake_hass = SimpleNamespace(data={})
    assert get_zigpy_app(fake_hass) is None  # type: ignore[arg-type]


def test_specs_default_includes_koenkk_and_zigpy() -> None:
    """By default both reliable community indexes are included."""
    specs = build_provider_specs({})
    assert ("z2m", Z2M_KOENKK_INDEX_URL) in specs
    assert ("z2m", ZIGPY_OTA_INDEX_URL) in specs


def test_specs_sources_can_be_disabled() -> None:
    """Disabling both built-in sources leaves them out."""
    specs = build_provider_specs({"use_koenkk": False, "use_zigpy": False})
    assert specs == []


def test_invalid_urls_flags_bad_entries() -> None:
    """Non-http(s) entries are reported; blanks and valid URLs are not."""
    raw = "https://ok/index.json\nftp://nope\n  \nnot-a-url\nhttp://ok2"
    assert invalid_urls(raw) == ["ftp://nope", "not-a-url"]
    assert invalid_urls("") == []


def test_validate_folder(tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Absolute creatable paths pass; relative paths fail."""
    target = tmp_path / "ota" / "images"
    assert validate_folder(str(target)) is True
    assert target.is_dir()
    assert validate_folder("relative/path") is False


def test_specs_extra_urls_and_local_folder() -> None:
    """Extra URLs (one per line, blanks ignored) and a local folder are added."""
    specs = build_provider_specs(
        {
            "use_koenkk": False,
            "use_zigpy": False,
            "extra_urls": "https://a/index.json\n   \nhttps://b/index.json",
            "local_folder": " /config/zigbee_ota ",
        }
    )
    assert ("z2m", "https://a/index.json") in specs
    assert ("z2m", "https://b/index.json") in specs
    assert ("advanced", "/config/zigbee_ota") in specs
