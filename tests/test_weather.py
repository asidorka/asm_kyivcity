"""Tests for GisMeteo integration."""
from asynctest import Mock
from homeassistant.components.weather import DOMAIN as WEATHER_DOMAIN
from homeassistant.const import CONF_NAME, CONF_PLATFORM
from homeassistant.core import HomeAssistant
from homeassistant.setup import async_setup_component
from pytest_homeassistant_custom_component.common import assert_setup_component

from custom_components.asmkyivcity import GismeteoDataUpdateCoordinator
from custom_components.asmkyivcity.const import DOMAIN
from custom_components.asmkyivcity.weather import GismeteoWeather

from tests.const import MOCK_UNIQUE_ID


async def test_entity_initialization(hass: HomeAssistant):
    """Test sensor initialization."""
    mock_api = Mock()
    mock_api.condition = Mock(return_value="asd")
    mock_api.attributes = {}

    coordinator = GismeteoDataUpdateCoordinator(hass, MOCK_UNIQUE_ID, mock_api)
    entity = GismeteoWeather("Test", coordinator)

    assert entity.name == "Test"
    assert entity.unique_id == MOCK_UNIQUE_ID


async def test_async_setup_platform(hass: HomeAssistant, gismeteo_api):
    """Test platform setup."""
    config = {
        WEATHER_DOMAIN: {
            CONF_PLATFORM: DOMAIN,
            CONF_NAME: "Office",
        },
    }

    with assert_setup_component(1, WEATHER_DOMAIN):
        assert await async_setup_component(hass, WEATHER_DOMAIN, config)
    await hass.async_block_till_done()

    state = hass.states.get(f"{WEATHER_DOMAIN}.office")
    assert state is not None
    assert state.state == "snowy"
