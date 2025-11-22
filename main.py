from llama_cpp import Llama
import os
import config

max_threads = os.cpu_count()
if config.number_of_threads > max_threads:
    config.number_of_threads = max_threads

llm = Llama(
    model_path=config.path_to_model,
    n_ctx=config.max_context_size,
    n_threads=config.number_of_threads,
    verbose=config.verbose_warnings,
)

messages = [config.bot["system_prompt"]]
messages_all = [config.bot["system_prompt"]]
print("*** Chat — type 'exit' to quit. ***\n")


while True:
    user_input = input("You: ")
    if user_input.lower() in {"exit", "quit"}:
        break

    # keep track of user input
    messages.append({"role": "user", "content": user_input})

    # call the LLM and generate response
    output = llm.create_chat_completion(
        messages=messages,
        max_tokens=config.max_tokens_per_response,
        temperature=config.temperature,
        top_p=config.top_p,
        top_k=config.top_k,
    )
    choice = output["choices"][0]["message"]
    output_text = (choice.get("content") or "").strip()
    if not output_text:
        output_text = "[No response generated.]"

    # keep track of bot responses
    messages.append({"role": "assistant", "content": output_text})

    # to keep responses faster, limit the number of messages we put in the context
    if len(messages) > config.messages_to_keep_in_context:
        if config.messages_to_keep_in_context == 0:
            messages = [config.bot["system_prompt"]]
        else:
            messages = [config.bot["system_prompt"]] + messages[-config.messages_to_keep_in_context:]

    # Display response
    print("\n")
    print(config.bot["name"] + ":", output_text)
    print("\n")