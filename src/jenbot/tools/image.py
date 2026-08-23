from pathlib import Path
import datetime
import uuid

from jenbot.tools.registry import register
from imagejenerator import registry


@register("image")
class ImageGenerationTool:

    def __init__(self, params):
        self.name = "image generator"
        self.config = params
        print(self.config)
        self.description = "Image generation via a diffusion model"
        self.generator = self.load_generator()
        self.output_path = self.config["output_folder"]
        self.image_location_messages = {
            "web": "Please inform the user that they can now view the images in the web interface. They will appear below your next reply.",
            "api": "Please inform the user that they can now view the images in the web interface. They will appear below your next reply.",
            "tui": f"The user can access the image/s in this folder {self.output_path}",
        }


    def load_generator(self):
        image_generator = registry.get_model_class(self.config)
        image_generator.load()
        image_generator.prepare()
        return image_generator


    def run(self, intent):

        response = None
        artifact_records = []
        self.generator.prompts = [intent["parameters"]["prompt"]]
        try:
            self.generator.prepare()
            output = self.generator.generate()
            ts = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
            for image in output.batch:
                path = Path(self.output_path)
                filename = f"{ts}_{str(uuid.uuid4())[:8]}.png"
                full_path = path / filename
                image.data.save(full_path)
                artifact_records.append({
                    "artifact_id": str(uuid.uuid4()),
                    "message_id": intent["message_id"],
                    "artifact_type": "image",
                    "path": str(full_path),
                })
        except Exception as e:
            return {
                "name": self.name,
                "description": self.description,
                "status": "failure",
                "output": f"Image generation tool error: {e}"
            }
        
        number_of_images = len(output.batch)
        image_wording = "1 image" if number_of_images == 1 else f"{number_of_images} images"
        print("PARAMETERS")
        print(intent)
        return {
            "name": self.name,
            "description": self.description,
            "status": "success",
            "output": f"""You have called the image generator tool and generated {image_wording}. You used the following image generation prompts: \n {'\n'.join(self.generator.config["prompts"])} \n {self.image_location_messages[intent["parameters"]["message"]["source"]]}""",
            "artifacts": artifact_records
        }