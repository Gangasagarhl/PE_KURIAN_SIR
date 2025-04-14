from transformers import T5Tokenizer, T5ForConditionalGeneration
import os
class Summarizer:
    def __init__(self,model,tokenizer):
        self.tokenizer = tokenizer
        self.model = model

    def summarize_chunk(self, text, max_length=150, min_length=30):
        input_text = "summarize: " + text.strip()
        inputs = self.tokenizer.encode(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )
        summary_ids = self.model.generate(
            inputs,
            max_length=max_length,
            min_length=min_length,
            length_penalty=2.0,
            num_beams=4,
            early_stopping=True
        )
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)

    def refine_summarize(self, captions):
        assert isinstance(captions, list), "Captions should be a list of strings"
        # Filter out very short captions
        filtered = [c.strip() for c in captions if len(c.strip()) > 10]

        if not filtered:
            return "No valid captions to summarize."

        # Start with the first caption
        refined_summary = self.summarize_chunk(filtered[0])

        for i, caption in enumerate(filtered[1:], start=2):
            combined = f"""
            Existing Summary: {refined_summary}
            New Caption: {caption}
            Update the summary if needed.
            """
            refined_summary = self.summarize_chunk(combined)
            print(f"🔸 Refined after caption {i}:\n", refined_summary)

        return refined_summary
