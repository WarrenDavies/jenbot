# technical set up

# If you're bringing your own model, add the path below
# If building the Docker container:
# - put your model into app/models so that it will be copied into the container
# - if using one from huggingface just add its name
path_to_model = "./models/bartowski/Llama-3.2-3B-Instruct-GGUF/Llama-3.2-3B-Instruct-Q4_K_L.gguf"
max_context_size = 4096 # total tokens allowable in the context
number_of_threads = 8 # number of CPU threads to use 
verbose_warnings = False # Silence llama_cpp warnings/messages


# Bot response config

messages_to_keep_in_context = 4 # without a GPU, responses will get slower and slower as the context grows. You also might get an out of memory error if the context grows too big.
# To keep Jenbot responding quickly, you can keep only the most recent n messages with this variable. This includes the system prompt, which will always remain in the context. If you put 0, you'll only get the system prompt, essentially wiping Jenbot's memory after every response.
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
            "content": """You are Jenbot, an expert, helpful, and diligent assistant. You provide the user with accurate answers to their queries. You are polite, friendly, and a little sarcastic."""
        }
    },
    "roastbot": {
        "name": "Jenbot",
        "system_prompt": {
            "role": "system", 
            "content": """You are RoastBot, queen of sarcasm. You are the meanest mudsucker in the world. Your goal is to be as unhelpful, sarcastic, insulting, and mean as possible. These dumb users, coming at you asking questions, wanting your help, and giving nothing back. Well they're about to get something back! Let them have it! Crush them with your wit! Shower them in misinformation! Treat them like children! Shout! Swear! Destroy!...roast."""

        }
    }
}


# Choose the bot that you want to use here.
bot = bots["roastbot"]