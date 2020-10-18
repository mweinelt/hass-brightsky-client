from datetime import datetime, timedelta
from hass_brightsky_client import BrightSkyDataProvider, CONDITION_MAP

LAT = 50.7
LNG = 7.1

MODE_DAILY = "daily"
MODE_WEEKLY = "weekly"


def test_current():
    weather = BrightSkyDataProvider(LAT, LNG, MODE_DAILY)
    weather.update_current()

    assert weather.current.get("icon") in CONDITION_MAP.values()


def test_forecast():
    weather = BrightSkyDataProvider(LAT, LNG, MODE_WEEKLY)

    begin = datetime.now()
    end = begin + timedelta(days=7)
    weather.update_forecast(begin, end)

    assert all(item.get("icon") in CONDITION_MAP.values() for item in weather.forecast)
