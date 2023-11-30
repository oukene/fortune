"""Config flow for Hello World integration."""
from homeassistant.helpers import selector
from homeassistant.helpers.selector import EntityFilterSelectorConfig
import logging
import voluptuous as vol
from typing import Any, Dict, Optional
from datetime import datetime


from homeassistant.helpers import (
    device_registry as dr,
    entity_registry as er,
)

import homeassistant.helpers.config_validation as cv

from homeassistant.helpers.device_registry import (
    async_get,
    async_entries_for_config_entry
)

from .const import *

from homeassistant import config_entries, exceptions
from homeassistant.core import callback


_LOGGER = logging.getLogger(__name__)


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Hello World."""

    VERSION = 1
    CONNECTION_CLASS = config_entries.CONN_CLASS_LOCAL_POLL
    data: Optional[Dict[str, Any]]

    async def async_step_user(self, user_input: Optional[Dict[str, Any]] = None):
        """Handle the initial step."""
        errors = {}
        if user_input is not None:
            self.data = user_input
            return self.async_create_entry(title=NAME, data=self.data)

        # If there is no user input or there were errors, show the form again, including any errors that were found with the input.
        return self.async_show_form(
            step_id="user", data_schema=vol.Schema(
                {

                }), errors=errors
        )

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Handle a option flow."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Handles options flow for the component."""

    def __init__(self, config_entry) -> None:
        self.config_entry = config_entry
        self._selected_option = {}
        # self.data = {}
        # self.data[CONF_ZODIAC] = config_entry.options.get(CONF_ZODIAC, [])
        # self.data[CONF_CONSTELLATION] = config_entry.options.get(CONF_CONSTELLATION, [])

    async def async_step_init(
        self, user_input: Dict[str, Any] = None
    ) -> Dict[str, Any]:
        """Manage the options for the custom component."""
        errors: Dict[str, str] = {}

        if user_input is not None:
            options = {}
            options[CONF_ZODIAC] = user_input.get(CONF_ZODIAC)
            options[CONF_CONSTELLATION] = user_input.get(
                CONF_CONSTELLATION, [])
            options[CONF_REFRESH_INVERVAL] = user_input.get(
                CONF_REFRESH_INVERVAL,[])

            for enable in ENABLE_FORTUNE_LIST.values():
                _LOGGER.debug("enable value : " + str(enable))
                options[enable] = user_input.get(enable, False)

            return self.async_create_entry(title=NAME, data=options)

        options_schema = vol.Schema(
            {
                vol.Optional(CONF_ZODIAC, description={"suggested_value": self.config_entry.options.get(CONF_ZODIAC, None)}): selector.SelectSelector(selector.SelectSelectorConfig(options=list(ZODIAC_LIST.keys()), custom_value=True, multiple=True,
                                                                                                                                                                    mode=selector.SelectSelectorMode.DROPDOWN, translation_key=CONF_ZODIAC)),
                vol.Optional(CONF_CONSTELLATION, description={"suggested_value": self.config_entry.options.get(CONF_CONSTELLATION, None)}): selector.SelectSelector(selector.SelectSelectorConfig(options=list(CONSTELLATION_LIST.keys()), custom_value=True, multiple=True,
                                                                                                                                                                mode=selector.SelectSelectorMode.DROPDOWN, translation_key=CONF_CONSTELLATION)),
                vol.Optional(CONF_REFRESH_INVERVAL, description={"suggested_value": self.config_entry.options.get(CONF_REFRESH_INVERVAL, DEFAULT_REFRESH_INTERVAL)}): selector.NumberSelector(selector.NumberSelectorConfig(min=0, max=600, mode=selector.NumberSelectorMode.BOX)),
                vol.Optional(ENABLE_FORTUNE_LIST[TODAY], description={"suggested_value": self.config_entry.options.get(ENABLE_FORTUNE_LIST[TODAY], False)}): selector.BooleanSelector(selector.BooleanSelectorConfig()),
                vol.Optional(ENABLE_FORTUNE_LIST[TOMORROW], description={"suggested_value": self.config_entry.options.get(ENABLE_FORTUNE_LIST[TOMORROW], False)}): selector.BooleanSelector(selector.BooleanSelectorConfig()),
                vol.Optional(ENABLE_FORTUNE_LIST[WEEK], description={"suggested_value": self.config_entry.options.get(ENABLE_FORTUNE_LIST[WEEK], False)}): selector.BooleanSelector(selector.BooleanSelectorConfig()),
                vol.Optional(ENABLE_FORTUNE_LIST[MONTH], description={"suggested_value": self.config_entry.options.get(ENABLE_FORTUNE_LIST[MONTH], False)}): selector.BooleanSelector(selector.BooleanSelectorConfig()),
            }
        )
        
        return self.async_show_form(
            step_id="init", data_schema=options_schema, errors=errors
        )


class CannotConnect(exceptions.HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidHost(exceptions.HomeAssistantError):
    """Error to indicate there is an invalid hostname."""
