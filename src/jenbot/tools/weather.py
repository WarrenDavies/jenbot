import requests

from jenbot.tools.registry import register


@register("weather")
class WeatherTool:

    def __init__(self):
        self.name = "weather"


    def run(self, parameters):
        current = ["temperature_2m", "apparent_temperature", "is_day", "rain", "weather_code", "wind_speed_10m", "cloud_cover", "showers", "precipitation"]
        base_url = "https://api.open-meteo.com/v1/forecast"
        params = {
            "latitude": 51.53,
            "longitude": -0.14,
            "current": current,
            "forecast_days": 1,
        }

        response = None
        try:
            response = requests.get(base_url, params=params)
            response.raise_for_status()
        except requests.exceptions.RequestException as e:
            return {
                "name": self.name,
                "status": "failure",
                "output": f"API request failed with exception: {e}"
            }

        data = response.json()
        
        metrics = []
        for metric in current:
            metrics.append(
                f"""{metric}: {data["current"][metric]} {data["current_units"][metric]}"""
            )
        metrics_str = "\n".join(metrics)

        return {
            "name": self.name,
            "status": "success",
            "output": metrics_str
        }