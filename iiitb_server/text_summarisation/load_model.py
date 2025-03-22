from transformers import T5Tokenizer, T5ForConditionalGeneration

# Define Local Path
class model_load:
    def model_load(self):
        local_model_path = "./local_models/t5-large"
        

        # Load Model & Tokenizer from Local Storage
        tokenizer = T5Tokenizer.from_pretrained(local_model_path)
        model = T5ForConditionalGeneration.from_pretrained(local_model_path)

        #print("Model loaded from local directory successfully!")
        return tokenizer, model


