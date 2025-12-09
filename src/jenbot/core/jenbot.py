import os
import copy

from src.jenbot.config import config
from imagejenerator.models import registry as image_registry
from textjenerator.models import registry as llm_registry


class Jenbot():
    """
    
    """

    def __init__(self, config = config):
        """
        Initializes the object with a config.

        Args:
            config (dict): A dictionary containing configuration parameters.
                Expected keys include:
                - 
        """
        self.config = config
        self.messages_all = [config["bot"]["system_prompt"]]
        self.messages_rolling = [config["bot"]["system_prompt"]]
        self.text_generator = None
        self.load_llm()
        self.activate()


    def load_llm(self):
        print(self.config["llm_config"])
        self.text_generator = llm_registry.get_model_class(self.config["llm_config"])
        self.text_generator.create_pipeline()
        print(self.text_generator)


    def generate_image(self, message):
        print("generating image")
        prompt = message[6:]
        print(prompt)
        config["image_config"]["prompts"][0] = prompt
        image_generator = image_registry.get_model_class(self.config["image_config"])
        image_generator.generate_image()


    def save_(self):
        """
        #### rename to save_image, save_text, save_speeh... etc.

        Saves generated XXXX to the configured directory with a timestamped filename.

        """
        self.save_timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
        file_name = f"{self.save_timestamp}.png"
        save_path = os.path.join(self.config["save_folder"], file_name)
        output.save(save_path)


    # def complete_generation_record(self):
    #     """
    #     Populates the generation record with metadata.

    #     Args:
    #     """
    #     self.generation_record.gen_data_file_path = self.config["gen_data_file_path"]
    #     self.generation_record.filename = f"{self.save_timestamp}.png"
    #     self.generation_record.timestamp = self.save_timestamp
    #     self.generation_record.model = self.config["model"]
    #     self.generation_record.device = self.device
    #     self.generation_record.dtype = self.config["dtype"]
    #     self.complete_generation_record_impl()


    # @abstractmethod
    # def complete_generation_record_impl(self):
    #     """
    #     Abstract hook for subclasses to add model-specific statistics to the record.
    #     """
    #     pass


    # def save_gen_stats(self):
    #     """
    #     Saves metadata to the record file.
    #     """
    #     self.complete_generation_record(prompt, i)
    #     self.generation_record.save_data()


    def activate(self):
        while True:
            user_input = input("You: ")
            if user_input.lower() in {"exit", "quit"}:
                break

            if user_input[0:5] == "IMAGE":
                try:
                    self.generate_image(user_input)
                    continue
                except Exception as e:
                    print("failed: ", e)
                    continue

            # keep track of user input
            self.messages_rolling.append({"role": "user", "content": user_input})
            self.messages_all.append({"role": "user", "content": user_input})

            llm_params = copy.deepcopy(self.config["llm_config"])
            messages = {"messages": self.messages_rolling}
            # call the LLM and generate response
            output_text = self.text_generator.run_pipeline(messages)

            output_text_lines = output_text.split("\n")
            for output_text_line in output_text_lines:
                if output_text_line[0:5] == "IMAGE":
                    try:
                        self.generate_image(output_text_line)
                    except Exception as e:
                        print("failed: ", e)
            
            # keep track of bot responses
            self.messages_rolling.append({"role": "assistant", "content": output_text})
            self.messages_all.append({"role": "assistant", "content": output_text})

            # to keep responses faster, limit the number of messages we put in the context
            if len(messages) > config["llm_config"]["messages_to_keep_in_context"]:
                if config["llm_config"]["messages_to_keep_in_context"] == 0:
                    messages = [config.bot["system_prompt"]]
                else:
                    messages = [config.bot["system_prompt"]] + messages[-config["llm_config"]["messages_to_keep_in_context"]:]

            # Display response
            print("\n")
            print(config["bot"]["name"] + ":", output_text)
            print("\n")

