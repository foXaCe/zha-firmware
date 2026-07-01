"""Config and options flow for the ZHA Firmware OTA Manager integration."""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult, OptionsFlow
from homeassistant.core import callback
from homeassistant.helpers import selector
import voluptuous as vol

from .const import (
    CONF_BROADCAST,
    CONF_EXTRA_URLS,
    CONF_LOCAL_FOLDER,
    CONF_USE_KOENKK,
    CONF_USE_ZIGPY,
    DEFAULT_BROADCAST,
    DEFAULT_USE_KOENKK,
    DEFAULT_USE_ZIGPY,
    DOMAIN,
    INTEGRATION_NAME,
    ZHA_DOMAIN,
)

if TYPE_CHECKING:
    from collections.abc import Mapping

    from homeassistant.config_entries import ConfigEntry


def _options_schema(options: Mapping[str, Any]) -> vol.Schema:
    """Build the options form schema, pre-filled with the current values."""
    return vol.Schema(
        {
            vol.Required(
                CONF_USE_KOENKK,
                default=options.get(CONF_USE_KOENKK, DEFAULT_USE_KOENKK),
            ): selector.BooleanSelector(),
            vol.Required(
                CONF_USE_ZIGPY,
                default=options.get(CONF_USE_ZIGPY, DEFAULT_USE_ZIGPY),
            ): selector.BooleanSelector(),
            vol.Optional(
                CONF_EXTRA_URLS,
                default=options.get(CONF_EXTRA_URLS, ""),
            ): selector.TextSelector(selector.TextSelectorConfig(multiline=True)),
            vol.Optional(
                CONF_LOCAL_FOLDER,
                default=options.get(CONF_LOCAL_FOLDER, ""),
            ): selector.TextSelector(),
            vol.Required(
                CONF_BROADCAST,
                default=options.get(CONF_BROADCAST, DEFAULT_BROADCAST),
            ): selector.BooleanSelector(),
        }
    )


class ZhaFirmwareConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ZHA Firmware OTA Manager."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step (single instance, requires ZHA)."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if not self.hass.config_entries.async_entries(ZHA_DOMAIN):
            return self.async_abort(reason="zha_not_configured")

        if user_input is not None:
            return self.async_create_entry(
                title=INTEGRATION_NAME,
                data={},
                options={
                    CONF_USE_KOENKK: DEFAULT_USE_KOENKK,
                    CONF_BROADCAST: DEFAULT_BROADCAST,
                },
            )

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))

    @staticmethod
    @callback
    def async_get_options_flow(
        config_entry: ConfigEntry,
    ) -> ZhaFirmwareOptionsFlow:
        """Return the options flow handler."""
        return ZhaFirmwareOptionsFlow()


class ZhaFirmwareOptionsFlow(OptionsFlow):
    """Handle the options flow (manage OTA sources)."""

    async def async_step_init(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Manage the OTA sources."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        return self.async_show_form(
            step_id="init",
            data_schema=_options_schema(self.config_entry.options),
        )
