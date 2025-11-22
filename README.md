# Jenbot

Jenbot is a local LLM assistant.

This is Jenbot Mk1: *"Built in a cave, with a box of scraps"*

Jenbot Mk1 runs on CPU only, and in the terminal - no fancy-dancy UI to hog your resources. Should run on your crappy old laptop.

## Quick start

```sh
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
hf download bartowski/Llama-3.2-3B-Instruct-GGUF --include="Llama-3.2-3B-Instruct-Q4_K_L.gguf" --local-dir ./models/bartowski/Llama-3.2-3B-Instruct-GGUF
python main.py
```

## Config

You can tweak a few things in config.py

#### **Technical settings**
* **path_to_model**: see notes below
* **max_context_size**: total tokens allowable in the context
* **number_of_threads**: number of CPU threads to use 
* **verbose_warnings**: Silence llama_cpp warnings/messages. Keep this False

#### **Bot settings**
* **messages_to_keep_in_context**: Responses get slower and slower as the context grows. Without a GPU, you might get to 5-10 minutes per reply within 5-6 messages. You also might get an out of memory error if the context grows too big. To keep Jenbot responding quickly, you can keep only the most recent n messages with this variable. This includes the system prompt, which will always remain in the context. If you put 0, you'll only get the system prompt, essentially wiping Jenbot's memory after every response.
* **max_tokens_per_response**: Max length for Jenbot's replies. If you find the responses get cut off mid-sentence, try increasing this to 512, or adjust the system prompt to tell her to be more concise.
* **temperature**, **top_p**, **top_k**: Higher values mean more creative, more varied, and less predictable responses. Go too high, however, and Jenbot will devolve into madness.

#### **Bots**
* **bots**: Create your own bots with their own system prompts here.
* **bot**: Choose which bot from the bots dictionary you want to use. Change this to `roastbot` if you want a more abrasive experience.

## Running locally (or in Codespaces)

### Set up the environment

Set up your Python environement and install dependencies:

```py
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Installing a model

You can only use the Llama LLMs with Jenbot Mk1, and as this is CPU only you're probably looking at 1B or  3B 4-bit quantised models. 

A 3B 4-bit quantised is installed by default. If this is too slow, or if you just want to try a different model:

1) Download the GGUF file of the model you want to try, (either manually download it from Hugging Face or use the Hugging Face CLI - examples below)
2) Move the GGUF file into the `./models` folder (the Hugging Face CLI can do this automatically)
3) Update `path_to_model` in `config.py` and point it to the GGUF file (e.g., `path_to_model = "./models/Llama-3.2-3B-Instruct-Q4_K_L.gguf"`)


#### Examples:

Default model:
```
hf download bartowski/Llama-3.2-3B-Instruct-GGUF --include="Llama-3.2-3B-Instruct-Q4_K_L.gguf" --local-dir ./models/bartowski/Llama-3.2-3B-Instruct-GGUF
```

A 1B model:
```
hf download bartowski/Llama-3.2-1B-Instruct-GGUF --include="Llama-3.2-1B-Instruct-Q4_K_L.gguf" --local-dir ./models/bartowski/Llama-3.2-1B-Instruct-GGUF
```

These are ~2.1GB and ~800MB respectively so may take a while to download.


## Running Jenbot

```py
python chat.py
```

Say `exit` to quit.


## Running in a Docker container

Run the instructions in the "Running locally", apart from `python chat.py`. 

Build the container:

`docker build -t jenbot:v1.0 .`

Run the container:

`docker run -it --rm --network none jenbot:v1.0 /bin/bash`

Vim is installed in the docker so you can edit the config while the container is running if you wish. You'll need to commit your changes to persist them though.

Then run Jenbot once you're inside the container:

`python app/main.py`
