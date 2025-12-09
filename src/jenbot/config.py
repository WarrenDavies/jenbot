# technical set up

# If you're bringing your own model and running on your local system, add the path to the model's GGUF below
# If building the Docker container:
# - the model gets copied into the container, so you must copy the GGUF into ./models
# - OR... if you know what you're doing, mount your cache folder to the container and point to that instead

# You can create your own bots here.
bots = {
    "jenbot": {
        "name": "Jenbot",
        "system_prompt": {
            "role": "system", 
            "content": """You are Jenbot, an expert, helpful, and diligent assistant. You provide the user with accurate answers to their queries. You are polite, friendly, and a little sarcastic.
            
            You can generate images if requested. To do so, use the command IMAGE on a new line, followed by the prompt. For example: 

IMAGE <your prompt>            

The image and the prompt need to be on the same line. You prompt should be a comma separated list of visual features. Use no more than 10.
            """
        }
    },
    "roastbot": {
        "name": "Roastbot",
        "system_prompt": {
            "role": "system", 
            "content": """You are RoastBot, queen of sarcasm. You are the meanest mudsucker in the world. Your goal is to be as unhelpful, sarcastic, insulting, and mean as possible. These dumb users, coming at you asking questions, wanting your help, and giving nothing back. Well they're about to get something back! Let them have it! Crush them with your wit! Shower them in misinformation! Treat them like children! Shout! Swear! Destroy!...roast."""

        }
    }
}

config = {

    "llm_config": {
        "model": "llama-cpp",
        "model_path": "./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf",
        
        "device": "cpu",
        "number_of_threads": 20,
        "n_gpu_layers": -1,
        
        "dtype": "float32",
        "max_context_size": 4096,
        "verbose_warnings": False,
        "messages_to_keep_in_context": 4,
        "max_tokens_per_response": 256 ,
        "temperature": 0.7 ,
        "top_p": 0.9,
        "top_k": 50,
    },
    "image_config": {
        "model": "stable-diffusion-v1-5",
        "model_path": "runwayml/stable-diffusion-v1-5",

        "device": "cuda",
        "enable_attention_slicing": True,
        "scheduler": "EulerDiscreteScheduler",

        "height": 512,
        "width": 512,
        "num_inference_steps": 30,
        "guidance_scale": 10,
        "images_to_generate": 1,
        "seeds": [], # leave empty for random
        "dtype": "bfloat16",


        "image_save_folder": "./images/",

        "save_image_gen_stats": True,
        "image_gen_data_file_path": "./stats/image_gen_stats.csv",

        "prompts": [
            "A rockstar playing a guitar solo on stage"
        ]
    }

}

# Choose the bot that you want to use here.
config["bot"] = bots["jenbot"]
config["llm_config"]["messages"] = [config["bot"]["system_prompt"]]


