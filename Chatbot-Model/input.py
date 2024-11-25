max_seq_length = 2048 # Choose any! We auto support RoPE Scaling internally!
dtype = None # None for auto detection. Float16 for Tesla T4, V100, Bfloat16 for Ampere+
load_in_4bit = False # Use 4bit quantization to reduce memory usage. Can be False.

from peft import AutoPeftModelForCausalLM
from transformers import AutoTokenizer
def chat():
    model = AutoPeftModelForCausalLM.from_pretrained(
        "D:\ProgrammingProject\chatbot\Chatbot-Model\lora_model", # YOUR MODEL YOU USED FOR TRAINING
        load_in_4bit = load_in_4bit,
    )
    tokenizer = AutoTokenizer.from_pretrained("D:\ProgrammingProject\chatbot\Chatbot-Model\lora_model")

    alpaca_prompt = """Below is an instruction that describes a task, paired with an input that provides further context. Write a response that appropriately completes the request.

    ### Instruction:
    {}

    ### Response:
    {}"""

    inputs = tokenizer(
    [
        alpaca_prompt.format(
            "What is a famous tall tower in Paris?", # instruction
            "", # input - leave this blank
            "", # output - leave this blank for generation!
        )
    ], return_tensors = "pt")

    from transformers import TextStreamer
    text_streamer = TextStreamer(tokenizer)
    _ = model.generate(**inputs, streamer = text_streamer, max_new_tokens = 128)


chat()