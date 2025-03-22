from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.prompts import PromptTemplate
from langchain.llms.ollama import Ollama  # Import the Ollama LLM wrapper
from text_processing_from_llm import format_text

from transformers import pipeline
summary = pipeline("summarization")

class GenerateSummary:
    @staticmethod
    def refine_summarization(chunks):
        """
        Generate a summary for the input text using the Refine approach,
        ensuring that the final summary has between 350 to 400 words using
        the Ollama llama3.2:1b model.
        """
        # Initialize the Ollama LLM with the llama3.2:1b model.
        llm = Ollama(model="llama3.2")
        
        # Convert text chunks into LangChain documents.
        documents = [Document(page_content=chunk) for chunk in chunks]
        
        # Define custom prompt templates for the refine chain.
        initial_prompt_template = (
            "You are an AI assistant tasked with summarizing events captured over a 12-hour period. "
            "Every 10 seconds, a new textual description of the scene has been recorded, forming a detailed sequence of observations. "
            "Your goal is to analyze this sequence and generate a concise summary as if you were an observer present for the entire 12 hours. "
            "The summary should highlight key events, notable patterns, and any significant occurrences, ensuring clarity and coherence. "
            "\n\n"
            "**Text Data:**\n{text}\n\n"
            "**Generate a well-structured summary based on the above observations.**"
        )

        refine_prompt_template = (
            "You are an AI assistant tasked with refining and expanding an existing summary based on newly received observations. "
            "Your goal is to seamlessly integrate the additional details into the summary while maintaining coherence, clarity, and a well-structured flow. \n\n"
            
            
            "**Existing Summary:**\n{existing_answer}\n\n"
            
            "**Additional Observations:**\n{text}\n\n"
            
            "**Task:** If the new observations provide meaningful updates, refine the summary accordingly. "
            "If the additional text does not contribute significantly, return the existing summary unchanged."
        )

        # Create PromptTemplate objects.
        initial_prompt = PromptTemplate(template=initial_prompt_template, input_variables=["text"])
        refine_prompt = PromptTemplate(template=refine_prompt_template, input_variables=["existing_answer", "text"])
        
        # Load the Refine summarization chain with the Ollama LLM.
        chain = load_summarize_chain(
            llm,
            chain_type="refine",
            question_prompt=initial_prompt,  # Used for initial summarization
            refine_prompt=refine_prompt      # Used to refine the summary with subsequent chunks
        )
        
        # Run the chain to generate the final summary.
        final_summary = chain.invoke({"input_documents": documents})
        
        text = format_text(final_summary['output_text'])

        # Save the final summary to a file.
        with open('summary.txt', 'w', encoding='utf-8') as f:
            f.write(text)
            
        return text

# Example usage:
# chunks = ["Text chunk 1", "Text chunk 2", ...]  # List of text chunks.
# summary = GenerateSummary.refine_summarization(chunks)
# print(summary)
