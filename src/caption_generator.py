import torch
from transformers import BlipProcessor, BlipForConditionalGeneration
from PIL import Image

# Load captioning model once
checkpoint_dir = "./notebook/blip-finetuned/checkpoint-6069"
device = "cuda" if torch.cuda.is_available() else "cpu"

processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
caption_model = BlipForConditionalGeneration.from_pretrained(checkpoint_dir)
caption_model.to(device) # type: ignore
# Ensure the model is in evaluation mode
caption_model.eval()

def get_caption(image):
    # Ensure processor is not overwritten and is a BlipProcessor instance
    inputs = processor(images=image, return_tensors="pt") # type: ignore
    inputs = {k: v.to(device) for k, v in inputs.items()}
    with torch.no_grad():
        output = caption_model.generate(**inputs, max_length=30, num_beams=5)

    raw_caption = processor.decode(output[0], skip_special_tokens=True) # type: ignore
    caption = raw_caption.strip().split(".")[0].replace("[", "").replace("'", "").replace(",", "").strip() + "."
    return caption
