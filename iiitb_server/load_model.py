from transformers import T5Tokenizer, T5ForConditionalGeneration

# Define Local Path
def model_load():
    local_model_path = "./local_models/t5-base"

    # Load Model & Tokenizer from Local Storage
    tokenizer = T5Tokenizer.from_pretrained(local_model_path)
    model = T5ForConditionalGeneration.from_pretrained(local_model_path)

    #print("Model loaded from local directory successfully!")
    return tokenizer, model


