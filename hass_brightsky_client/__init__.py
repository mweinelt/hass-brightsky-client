import logging
import datetime
import requests
from urllib.parse import urljoin

_LOGGER = logging.getLogger(__name__)

API_URL = "https://api.brightsky.dev"
CONDITION_MAP = {
    "clear-day": "sunny",
    "clear-night": "clear-night",
    "partly-cloudy-day": "partlycloudy",
    "partly-cloudy-night": "clear-night",  # or partlycloudy?
    "cloudy": "cloudy",
    "fog": "fog",
    "wind": "windy",
    "rain": "rainy",
    "sleet": "snowy-rainy",
    "snow": "snowy",
    "hail": "hail",
    "thunderstorm": "lightning",
}


class BrightSkyDataProvider:
    """Get the latest data from Bright Sky."""

    def __init__(self, latitude: float, longitude: float, mode: str) -> None:
        """Initialize the Bright Sky Weather Provider."""
        self.latitude = latitude
        self.longitude = longitude
        self.mode = mode

        self.current = None
        self.forecast = []

    def update_current(self) -> None:
        """Retrieve current weather data."""
        def hassify(current: dict) -> dict:
            # brightsky condition names to hass condition names
            current["icon"] = CONDITION_MAP.get(current.get("icon"))
            return current

        try:
            response = requests.get(
                urljoin(API_URL, "/current_weather"),
                params={"lat": self.latitude, "lon": self.longitude},
            )
            self.current = hassify(response.json()["weather"])
        except (requests.exceptions.RequestException, KeyError) as error:
            _LOGGER.error(
                "Unable to retrieve current weather from Bright Sky: %s", error
            )
            self.current = None

    def update_forecast(self, begin: datetime, end: datetime) -> None:
        """Retrieve forecast data."""
        def hassify(forecast: dict) -> dict:
            for item in forecast:
                item.update({"icon": CONDITION_MAP.get(item["icon"])})

            return forecast

        try:
            response = requests.get(
                urljoin(API_URL, "/weather"),
                params={
                    "lat": self.latitude,
                    "lon": self.longitude,
                    "date": begin.isoformat(),
                    "last_date": end.isoformat(),
                },
            ).json()

            self.forecast = hassify(response.get("weather"))
        except (requests.exceptions.RequestException, KeyError) as error:
            _LOGGER.error(
                "Unable to retrieve weather forecast from Bright Sky: %s", error
            )


