from datetime import date, timedelta
from typing import Any

from .service import Service, register_service
from dataclasses import dataclass
import requests

@register_service
@dataclass(kw_only=True)
class AirQuality(Service):
    token: str
    station_id: str = "10138"
    # This url queries the St Dominique Montreal
    _url: str = "https://api.waqi.info/feed/@{station_id}/?token={token}"

    def query(self)-> dict[str, Any]:
        response = requests.get(self._url.format(station_id=self.station_id, token=self.token))
        response.raise_for_status()
        json_data = response.json()

        if json_data.get("status") != "ok":
            print(f"Error fetching data for: {json_data.get('data')}")
            return {}


        data : dict[str, Any] = json_data["data"]

        # Calculate target historical date window
        today = date.today()
        uv_forecast = {}
        for item in  data.get("forecast", {}).get("daily", {}).get("uvi", {}):
            if item.get("day") == today.strftime("%Y-%m-%d"):
                uv_forecast = item
                break
        max_uv_index_forecast = uv_forecast.get("max", {})
        min_uv_index_forecast = uv_forecast.get("min", {})

        results = {
            "dominant_pollutant": data.get("dominentpol"),
            "air_quality_index": data.get("aqi"),
            "carbon_monoxide": data["iaqi"].get("co"),
            "nitrogen_dioxide": data["iaqi"].get("no2"),
            "ozone": data["iaqi"].get("o3"),
            "sulfur_dioxide": data["iaqi"].get("so2"),
            "fine_particulate_matter": data["iaqi"].get("pm25"),
            "coarse_particulate_matter" : data["iaqi"].get("pm10"),
            "temperature": data["iaqi"].get("t"), # Celsius
            "wind_speed": data["iaqi"].get("w"), # m/s?
            "wind_gust" : data["iaqi"].get("wg"), # same?
            "relative_humidity": data["iaqi"].get("h"), # percent
            "precipitation": data["iaqi"].get("p"), # hPa/mb
            "forecast_uv_index_max": max_uv_index_forecast,
            "forecast_uv_index_min": min_uv_index_forecast,
            "date": today,
        }
        return results