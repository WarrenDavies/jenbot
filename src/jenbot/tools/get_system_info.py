from jenbot.tools.registry import register


@register("get_system_info")
class GetSystemInfo:

    def __init__(self):
        self.name = "get_system_info"
        self.description = "Get information on the current state of the system, e.g., CPU temp, memory usage."


    def run(self, parameters):

        system_info = """{
            "CPU temp": "39 C",
            "RAM usage": 13.6 GB / 33.2 GB,
            "User active window": "Firefox | YouTube",
        }"""

        return {
            "name": self.name,
            "description": self.description,
            "status": "success",
            "output": system_info
        }
        
