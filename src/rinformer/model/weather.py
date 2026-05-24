from dataclasses import dataclass
from datetime import datetime, date, timedelta
from pprint import pprint
from typing import Any

from .service import Service, register_service
import requests



@register_service
@dataclass(kw_only=True)
class Weather:
    # Instead of filtering by ID text, we supply a tight bounding box around the CYUL instrument site.
    # Format: min_lon, min_lat, max_lon, max_lat
    _CYUL_BBOX: str = "-73.75,45.45,-73.73,45.48"

    # We use the bbox parameter and sort by the exact internal timestamp index: -date_tm-value
    _url: str = "https://api.weather.gc.ca/collections/swob-realtime/items?bbox={BBOX}&limit=1&sortby=-date_tm-value"

    def query(self) -> dict[str, Any]:
        print("Fetching active ECCC weather telemetry near Montreal (CYUL)...")
        url = self._url.format(BBOX=self._CYUL_BBOX)
        response = requests.get(url)
        if response.status_code == 200:
            data = response.json()
            if data.get("features"):
                # Get the single newest observational telemetry node
                latest_observation = data["features"][0]["properties"]

                # target values:
                result = {
                    "date_tm-value": latest_observation.get("date_tm-value"),  # UTC
                    "air_temperature": latest_observation.get("air_temp"),  # Centigrade
                    "rel_humidity": latest_observation.get("rel_hum"),  # relative humidity, percent
                    "wind_speed": latest_observation.get("wnd_spd"),  # win speed in km/h
                    "max_air_temperature_past_hour": latest_observation.get("max_air_temp_pst1hr"),  # Centigrade
                    "avg_air_temperature_past_hour": latest_observation.get("avg_air_temp_pst1hr"),  # Centigrade
                }
                return result
            else:
                print("No recent data features found for that Station ID.")
                return {}
        else:
            print(f"Failed to fetch. Status code: {response.status_code}")
            return {}