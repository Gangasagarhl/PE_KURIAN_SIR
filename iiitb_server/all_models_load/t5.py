from transformers import T5Tokenizer, T5ForConditionalGeneration

class t5_load:
    def __init__(self):
        model_name = "t5-base"
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        print("\n\n*********T5 MODEL DOWNLOADED*********\n\n")
        
        self.loaded = True
        print("\n✅✅✅ BLIP MODEL LOADED SUCCESSFULLY ✅✅✅\n")

    def is_ready(self):
        return self.loaded
        
