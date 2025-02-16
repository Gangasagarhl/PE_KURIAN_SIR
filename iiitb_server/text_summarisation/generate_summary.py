from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.docstore.document import Document
from langchain.chains.summarize import load_summarize_chain
from langchain.llms import HuggingFacePipeline
from langchain.prompts import PromptTemplate
from transformers import pipeline
from load_model import model_load

class generate_summary:
    # Load the model and tokenizer using your load_model utility.
    model_ = model_load()
    tokenizer, model = model_.model_load()
    
    # Create the HuggingFace pipeline for text2text generation.
    summarization_pipeline = pipeline("text2text-generation", model=model, tokenizer=tokenizer)
    
    # Wrap the pipeline with LangChain's HuggingFacePipeline.
    llm = HuggingFacePipeline(pipeline=summarization_pipeline)

    @staticmethod
    def split_text(text, chunk_size=450, overlap=50):
        """
        Split the text into chunks using LangChain's RecursiveCharacterTextSplitter.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        return text_splitter.split_text(text)

    @staticmethod
    def refine_summarization(text):
        """
        Generate a summary for the input text that is between 400 and 450 words.
        This is done by splitting the text into chunks and then running a refine summarization chain
        with custom prompt templates that instruct the model to produce a summary with the desired word count.
        """
        # Step 1: Split the input text into smaller chunks.
        chunks = generate_summary.split_text(text)
        documents = [Document(page_content=chunk) for chunk in chunks]


        # Step 2: Create custom prompt templates with explicit instructions on the summary length.
        initial_prompt_template = (
            "Write a comprehensive summary of the following text. "
            "The summary must be at least 400 words and no more than 450 words. "
            "Ensure all key points are covered.\n\n"
            "Text:\n{text}"
        )
        
        refine_prompt_template = (
            "You are given an existing summary:\n{existing_summary}\n\n"
            "Refine the summary using the additional context below. "
            "The final summary must be between 400 and 450 words and include all important points from the context.\n\n"
            "Additional Context:\n{text}\n\n"
            "Refined Summary:"
        )

        initial_prompt = PromptTemplate(
            template=initial_prompt_template,
            input_variables=["text"]
        )
        refine_prompt = PromptTemplate(
            template=refine_prompt_template,
            input_variables=["existing_summary", "text"]
        )

        # Step 3: Load the refinement summarization chain with the custom prompts.
        chain = load_summarize_chain(
            generate_summary.llm,
            chain_type="refine",
            question_prompt=initial_prompt,
            refine_prompt=refine_prompt
        )

        # Step 4: Run the chain on the documents to get the refined summary.
        refined_summary = chain.run(documents)
        return refined_summary


