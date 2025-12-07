# technical set up

# If you're bringing your own model and running on your local system, add the path to the model's GGUF below
# If building the Docker container:
# - the model gets copied into the container, so you must copy the GGUF into ./models
# - OR... if you know what you're doing, mount your cache folder to the container and point to that instead
path_to_model = "./models/Llama-3.2-3B-Instruct-Q4_K_M.gguf"
max_context_size = 4096 # total tokens allowable in the context
number_of_threads = 8 # number of CPU threads to use 
verbose_warnings = False # Silence llama_cpp warnings/messages


# Bot response config

messages_to_keep_in_context = 4 # Keep only the most recent n messages in the context (from either party, not pairs of messages), including the system prompt.
# This is because without a GPU, responses will get slower and slower as the context grows. You also might get an out of memory error if the context grows too big.
# To keep Jenbot responding quickly, we can continually trim the context. This means Jenbot will forget older messages. You can experiment with this to see what your system can handle before it slows to snail pace of you run out of RAM.
# If you put 0, you'll only get the system prompt, essentially wiping Jenbot's memory after every response.
max_tokens_per_response = 256 # Max length for Jenbot's replies. If you find the responses get cut off mid-sentence, try increasing this to 512, or adjust the system prompt to tell the bot to be more concise
# You can adjust the bot's behaviour with these settings. Higher values mean more creative, more varied, and less predictable responses. Go too high, however, and Jenbot will devolve into madness.
temperature = 0.7 
top_p = 0.9
top_k = 50


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

# Choose the bot that you want to use here.
bot = bots["jenbot"]

image_config = {
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