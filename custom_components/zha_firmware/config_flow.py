"""Config flow for the ZHA Firmware OTA Manager integration."""

from __future__ import annotations

from typing import Any

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
import voluptuous as vol

from .const import DOMAIN, INTEGRATION_NAME


class ZhaFirmwareConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for ZHA Firmware OTA Manager."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step (single instance)."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is not None:
            return self.async_create_entry(title=INTEGRATION_NAME, data={})

        return self.async_show_form(step_id="user", data_schema=vol.Schema({}))
