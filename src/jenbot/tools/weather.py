from jenbot.tools.registry import register



@register("weather")
class WeatherTool:

    def __init__(self):
        self.name = "weather"


    def run(self, parameters):
        return {
            "name": self.name,
            "status": "success",
            "output": f"The weather outside is frightful, but the fire is so delightful"
        }