from transformers import BlipProcessor, BlipForConditionalGeneration
class blip_load:
    def __init__(self):
        self.loaded = False  # Flag to track loading status
        print("⏳ Loading BLIP model...")

        model_name = "Salesforce/blip-image-captioning-base"
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

        self.loaded = True
        print("\n✅✅✅ BLIP MODEL LOADED SUCCESSFULLY ✅✅✅\n")

    def is_ready(self):
        return self.loaded
        