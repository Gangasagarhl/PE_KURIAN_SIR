from transformers import T5Tokenizer, T5ForConditionalGeneration

class ModelLoad:
    def model_load(self):
        # Specify the model name from Hugging Face Hub
        model_name = "t5-medium"
        
        # Load Model & Tokenizer from Hugging Face Hub
        tokenizer = T5Tokenizer.from_pretrained(model_name)
        model = T5ForConditionalGeneration.from_pretrained(model_name)

        #print("Model loaded from Hugging Face Hub successfully!")
        return tokenizer, model