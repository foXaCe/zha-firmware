"""Smoke tests for the integration manifest (no Home Assistant runtime needed)."""

from __future__ import annotations

import json
from pathlib import Path

MANIFEST = Path("custom_components/zha_firmware/manifest.json")


def test_manifest_is_valid() -> None:
    """The manifest is valid JSON with the expected core keys."""
    data = json.loads(MANIFEST.read_text(encoding="utf-8"))

    assert data["domain"] == "zha_firmware"
    assert data["version"]
    assert data["config_flow"] is True
    assert "zha" in data["after_dependencies"]
    assert data["codeowners"] == ["@foXaCe"]
    assert data["iot_class"] == "local_polling"


def test_translations_match_strings() -> None:
    """strings.json and every translation share the same key structure."""
    base = Path("custom_components/zha_firmware")
    strings = json.loads((base / "strings.json").read_text(encoding="utf-8"))

    def keys(node: object, prefix: str = "") -> set[str]:
        if not isinstance(node, dict):
            return {prefix}
        result: set[str] = set()
        for key, value in node.items():
            result |= keys(value, f"{prefix}.{key}" if prefix else key)
        return result

    expected = keys(strings)
    for lang in ("en", "fr"):
        translation = json.loads(
            (base / "translations" / f"{lang}.json").read_text(encoding="utf-8")
        )
        assert keys(translation) == expected, f"clés divergentes pour {lang}.json"
