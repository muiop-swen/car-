"""Binary sensor platform for Porsche Connect."""
import logging
from typing import Optional

from homeassistant.components.binary_sensor import BinarySensorEntity

from . import DOMAIN as PORSCHE_DOMAIN
from . import PorscheDevice
from .const import DEVICE_NAMES
from .const import HA_BINARY_SENSOR
from .const import SensorMeta

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Setup binary_sensor platform."""
    coordinator = hass.data[PORSCHE_DOMAIN][config_entry.entry_id]
    entities = []
    for vehicle in coordinator.vehicles:
        for sensor in vehicle["components"][HA_BINARY_SENSOR]:
            entities.append(PorscheBinarySensor(vehicle, coordinator, sensor))
    async_add_entities(entities, True)


class PorscheBinarySensor(PorscheDevice, BinarySensorEntity):
    """porscheconnect binary_sensor class."""

    def __init__(self, vehicle, coordinator, sensor_meta: SensorMeta):
        """Initialize of the sensor."""
        super().__init__(vehicle, coordinator)
        self.key = sensor_meta.key
        self.meta = sensor_meta
        device_name = DEVICE_NAMES.get(self.key, self.key)
        self._name = f"{self._name} {device_name}"
        self._unique_id = f"{super().unique_id}_{self.key}"

    @property
    def icon(self):
        """Return the icon of this entity."""
        return self.meta.icon

    @property
    def device_class(self) -> Optional[str]:
        """Return the device_class of the device."""
        return self.meta.device_class

    @property
    def is_on(self):
        """Return true if the binary_sensor is on."""
        data = self.coordinator.getDataByVIN(self.vin, self.key)
        return data == self.meta.isOnState
