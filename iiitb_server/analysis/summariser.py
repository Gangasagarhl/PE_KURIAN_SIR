import os
from iiitb_server.model_manage import t5_model, t5_tokenizer
from iiitb_server.analysis.summary_to_a_file import write_to_file

class Summarizer:
    def __init__(self):
        print("Summarizer called\n\n")

    def summarize_chunk(self, text, max_length=150, min_length=10):
        input_text = "summarize: " + text.strip()
        inputs = t5_tokenizer.encode(
            input_text,
            return_tensors="pt",
            max_length=512,
            truncation=True
        )
        summary_ids = t5_model.generate(inputs)
        return t5_tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    

    def map_reduce_summarize(self, captions):

        assert isinstance(captions, list), "Captions should be a list of strings"
        filtered = [c.strip() for c in captions if len(c.strip()) > 10]

        if not filtered:
            return "No valid captions to summarize."

        # Map Step: Summarize each caption
        print("\nIn Summaries generation\n")
        intermediate_summaries = []
        for i, caption in enumerate(filtered, start=1):
            summary = self.summarize_chunk(caption)
            intermediate_summaries.append(summary)
            print(f"🔹 Intermediate ready {i}:\n", summary)

        final_summary = self.refine_summarize(intermediate_summaries)

        # Reduce Step: Combine all intermediate summaries and summarize again
        combined_text = " ".join(intermediate_summaries)
        final_summary1 = self.summarize_chunk(combined_text)
        #print("\n\n\n\n\n\n**************** Final Map - Reduced Summary:*************\n", final_summary1)

        final_summary ="Refined: \n\n"+final_summary+"\n\n\nMap-Reduce Summary:\n"+final_summary1+"\n\n"

        #self.summarize_chunk()
        write_to_file().write(path = "Summary.txt", data=final_summary)

        return final_summary

    
    def refine_summarize(self, captions):
        print("\n In refine summaries\n")
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
            """
            refined_summary = self.summarize_chunk(combined)
            print(f"{i} Done:\n")

        #print("\n\n*****Refined Summary*****\n",refined_summary)
        return refined_summary