import os
from PIL import Image
import matplotlib.pyplot as plt
from src.caption_generator import get_caption
from src.quote_generator import generate_quote

image_dir = "./data/new_data/" # Directory containing new images

image_paths = sorted([
    os.path.join(image_dir, f)
    for f in os.listdir(image_dir)
    if f.endswith(('.jpg', '.png', '.jpeg'))
])[:5]

for i, path in enumerate(image_paths):
    image = Image.open(path).convert("RGB")

    # Display the image
    plt.imshow(image)
    plt.axis("off")
    plt.savefig(f"output_image_{i+1}.png")  # Save instead of show
    plt.close()
    print(f"Processing image: {path}")

    # Generate caption and quote
    caption = get_caption(image)
    quote = generate_quote(caption)

    print(f"Context ——> {caption}")
    print(f"Quotation ——> {quote}")
    print("-" * 50)

