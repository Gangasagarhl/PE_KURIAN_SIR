# model_manager.py
from transformers import BlipProcessor, BlipForConditionalGeneration, T5Tokenizer, T5ForConditionalGeneration

class BLIPLoader:
    def __init__(self):
        model_name = "Salesforce/blip-image-captioning-base"
        print("⏳ Loading BLIP model...")
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)
        print("✅ BLIP model loaded successfully.")
        
class T5Loader:
    def __init__(self):
        model_name = "t5-base"
        print("⏳ Loading T5 model...")
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        print("✅ T5 model loaded successfully.")

# Instantiate and expose the models
_blip_loader = BLIPLoader()
blip_model = _blip_loader.model
blip_processor = _blip_loader.processor

_t5_loader = T5Loader()
t5_model = _t5_loader.model
t5_tokenizer = _t5_loader.tokenizer
