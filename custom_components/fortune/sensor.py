"""Platform for sensor integration."""
# This file shows the setup for the sensors associated with the cover.
# They are setup in the same way with the call to the async_setup_entry function
# via HA from the module __init__. Each sensor has a device_class, this tells HA how
# to display it in the UI (for know types). The unit_of_measurement property tells HA
# what the unit is, so it can display the correct range. For predefined types (such as
# battery), the unit_of_measurement should match what's expected.
import logging
from threading import Timer
import aiohttp

import json
import asyncio

from .const import *
from homeassistant.helpers.entity import async_generate_entity_id
from homeassistant.components.sensor import SensorEntity
import requests
import aiohttp
import asyncio
from bs4 import BeautifulSoup as bs
import random
from datetime import datetime


_LOGGER = logging.getLogger(__name__)

# See cover.py for more details.
# Note how both entities for each roller sensor (battry and illuminance) are added at
# the same time to the same list. This way only a single async_add_devices call is
# required.

ENTITY_ID_FORMAT = DOMAIN + ".{}"
global total_size

async def async_setup_entry(hass, config_entry, async_add_devices):
    """Add sensors for passed config_entry in HA."""

    hass.data[DOMAIN]["listener"] = []

    device = Device(NAME)
    new_devices = []
    global total_size
    total_size = len(config_entry.options.get(CONF_ZODIAC, [])) + len(config_entry.options.get(CONF_CONSTELLATION, []))

    for key in config_entry.options.get(CONF_ZODIAC, []):
        new_devices.append(
            FortuneSensor(
                hass,
                device,
                CONF_ZODIAC,
                key,
                config_entry.options
            )
        )
    for key in config_entry.options.get(CONF_CONSTELLATION, []):
        new_devices.append(
            FortuneSensor(
                hass,
                device,
                CONF_CONSTELLATION,
                key,
                config_entry.options
            )
        )

    if new_devices:
        async_add_devices(new_devices)


class Device:
    """Dummy roller (device for HA) for Hello World example."""

    def __init__(self, name):
        """Init dummy roller."""
        self._id = name
        self.name = name
        self._callbacks = set()
        self._loop = asyncio.get_event_loop()
        # Reports if the roller is moving up or down.
        # >0 is up, <0 is down. This very much just for demonstration.

        # Some static information about this device
        self.firmware_version = VERSION
        self.model = NAME
        self.manufacturer = NAME

    @property
    def device_id(self):
        """Return ID for roller."""
        return self._id

    def register_callback(self, callback):
        """Register callback, called when Roller changes state."""
        self._callbacks.add(callback)

    def remove_callback(self, callback):
        """Remove previously registered callback."""
        self._callbacks.discard(callback)

    # In a real implementation, this library would call it's call backs when it was
    # notified of any state changeds for the relevant device.
    async def publish_updates(self):
        """Schedule call all registered callbacks."""
        for callback in self._callbacks:
            callback()

    def publish_updates(self):
        """Schedule call all registered callbacks."""
        for callback in self._callbacks:
            callback()

# This base class shows the common properties and methods for a sensor as used in this
# example. See each sensor for further details about properties and methods that
# have been overridden.


class SensorBase(SensorEntity):
    """Base representation of a Hello World Sensor."""

    should_poll = False

    def __init__(self, device):
        """Initialize the sensor."""
        self._device = device

    # To link this entity to the cover device, this property must return an
    # identifiers value matching that used in the cover, but no other information such
    # as name. If name is returned, this entity will then also become a device in the
    # HA UI.
    @property
    def device_info(self):
        """Information about this entity/device."""
        return {
            "identifiers": {(DOMAIN, self._device.device_id)},
            # If desired, the name for the device could be different to the entity
            "name": self._device.device_id,
            "sw_version": self._device.firmware_version,
            "model": self._device.model,
            "manufacturer": self._device.manufacturer
        }

    # This property is important to let HA know if this entity is online or not.
    # If an entity is offline (return False), the UI will refelect this.
    @property
    def available(self) -> bool:
        """Return True if roller and hub is available."""
        return True

    async def async_added_to_hass(self):
        """Run when this Entity has been added to HA."""
        # Sensors should also register callbacks to HA when their state changes
        self._device.register_callback(self.async_write_ha_state)

    async def async_will_remove_from_hass(self):
        """Entity being removed from hass."""
        # The opposite of async_added_to_hass. Remove any registered call backs here.
        self._device.remove_callback(self.async_write_ha_state)


class FortuneSensor(SensorBase):
    """Representation of a Thermal Comfort Sensor."""
    _attr_has_entity_name = True
    
    def __init__(self, hass, device, type, key, options):
        """Initialize the sensor."""
        super().__init__(device)

        self.hass = hass
        self._key = key
        self._type = type
        self._options = options
        self.entity_id = async_generate_entity_id(
            ENTITY_ID_FORMAT, "{}_{}".format(NAME, key), hass=hass, current_ids="")
        #self._attr_name = "{}-{}".format(key, FORTUNE_LIST[self._index])
        self._translation_key = key

        if CONF_ZODIAC == self._type:
            self.data_list = ZODIAC_LIST
        else:
            self.data_list = CONSTELLATION_LIST
        self._attr_entity_picture = ICON_URL_BASE + self.data_list[self._key][ICON]

        # self._device_class = SENSOR_TYPES[sensor_type][0]
        self._attr_unique_id = self.entity_id
        self._device = device
        self._loop = asyncio.get_event_loop()
        Timer(1, self.refreshTimer).start()

        self._extra_state_attributes = {}

        self._device.publish_updates()
    
    def refreshTimer(self):
        self._loop.create_task(self.get_fortune())
        Timer(self._options.get(CONF_REFRESH_INVERVAL)*60, self.refreshTimer).start()

    async def get_fortune(self):
        try:
            """"""
            headers = {
                "User-Agent": (
                    "mozilla/5.0 (windows nt 10.0; win64; x64) applewebkit/537.36 (khtml, like gecko) chrome/78.0.3904.70 safari/537.36"
                ),
                "Referer": (
                    "https://naver.com"
                )
            }

            self._attr_state = None
            url = BASE_URL + self.data_list[self._key]["kr_name"]
            _LOGGER.debug("url : " + str(url))
            _LOGGER.debug("total size : " + str(total_size))
            await asyncio.sleep(random.randrange(1, total_size))
            async with aiohttp.ClientSession(headers=headers) as session:
                async with session.get(url) as response:
                    raw_data = await response.read()
                    soup = bs(raw_data, 'html.parser')
                    index = 0
                    fortune_list = soup.select("._cs_fortune_text")
                    fortune_age = soup.select("._cs_fortune_list")
                    # _LOGGER.debug("age fortune : " + str(fortune_age))
                    for fortune in fortune_list:
                        _LOGGER.debug("fortune_age : " + str(fortune.text))
                        _LOGGER.debug("fortune_age length : " +
                                      str(len(fortune_age)))
                        
                        if self._options.get(ENABLE_FORTUNE_LIST[index], False):
                            self._extra_state_attributes[FORTUNE_LIST[index]] = fortune.text
                            if len(fortune_age) > index:
                                key = fortune_age[index].find_all("dt")
                                value = fortune_age[index].find_all("dd")
                                i = 0
                                for k in key:
                                    _LOGGER.debug("k : " + str(k.text) + ", v : " + str(value[i].text))
                                    self._extra_state_attributes[FORTUNE_LIST[index] +
                                                                "" + k.text] = value[i].text
                                    i+=1
                                # if index == 0 and self._ext_fortune == False:
                                #     break
                                total_size
                        index+=1
            self._attr_state = datetime.now().strftime("%Y-%m-%d %H:%M")
            self._device.publish_updates()
        except Exception as e:
            _LOGGER.error("get fortune error : " + str(e))
        
        finally:
            _LOGGER.debug("call next timer")
            #Timer(self._refresh_period*60, self._loop.create_task(self.get_price())).start()

    @property
    def translation_key(self) -> str | None:
        return self._translation_key

    @property
    def state(self):
        return self._attr_state

    @property
    def extra_state_attributes(self):
        return self._extra_state_attributes
