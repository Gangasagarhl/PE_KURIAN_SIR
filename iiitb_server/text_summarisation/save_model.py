from transformers import T5Tokenizer, T5ForConditionalGeneration

# Define Local Path to Store Model
local_model_path = "./local_models/t5-base"

# Load Pretrained Model and Tokenizer from Hugging Face
model_name = "t5-base"
tokenizer = T5Tokenizer.from_pretrained(model_name)
model = T5ForConditionalGeneration.from_pretrained(model_name)

# Save Model & Tokenizer Locally
tokenizer.save_pretrained(local_model_path)
model.save_pretrained(local_model_path)

print(f"Model and Tokenizer saved to {local_model_path}")
