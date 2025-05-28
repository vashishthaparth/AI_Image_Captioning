import re
import torch
from transformers import AutoModelForCausalLM, AutoTokenizer

model_path = "./notebook/models/mistral_models/7B-Instruct-v0.3/"

tokenizer = AutoTokenizer.from_pretrained(model_path)

model_Mistral = AutoModelForCausalLM.from_pretrained(
    model_path,
    torch_dtype=torch.float16,  # optional, use float16 if GPU supports
    device_map="auto",
    low_cpu_mem_usage=True
)

def generate_quote(caption):
    prompt = f"I have an image in which {caption}Generate a quotation around it."
    inputs = tokenizer(prompt, return_tensors="pt")
    inputs = {k: v.to(torch.long).to(model_Mistral.device) for k, v in inputs.items()}

    outputs = model_Mistral.generate(
        **inputs,
        max_new_tokens=500,
        pad_token_id=tokenizer.eos_token_id
    )
    raw_output = tokenizer.decode(outputs[0], skip_special_tokens=True)

    match = re.search(r'"(.*?)"', raw_output, re.DOTALL)
    return match.group(1) if match else "No quote generated."
