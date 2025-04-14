from transformers import BlipProcessor, BlipForConditionalGeneration
import warnings
import torch

warnings.filterwarnings("ignore")


local_path = "./blip_model"  # Replace with your actual path

processor = BlipProcessor.from_pretrained(local_path)
model = BlipForConditionalGeneration.from_pretrained(local_path)


#processor = BlipProcessor.from_pretrained("Salesforce/blip-image-captioning-base")
#model = BlipForConditionalGeneration.from_pretrained("Salesforce/blip-image-captioning-base")

def description(image):
    inputs = processor(images=image, return_tensors="pt")

    # Set min_length high enough (in tokens) to encourage longer outputs.
    # Note: min_length is in tokens, which may not exactly equal words.
    output = model.generate(
        **inputs, 
        #min_length=4,   # Increase token length to help yield at least 10 words
        #max_length=7,  
        #repetition_penalty=1.2,
        #num_beams=5
    )

    caption = processor.decode(output[0], skip_special_tokens=True)
    
    # Ensure the caption has at least 10 words. If not, append fallback text.
    """if len(caption.split()) < 10:
        caption += " The scene contains various objects and details that enhance its meaning.
        """

    return caption
