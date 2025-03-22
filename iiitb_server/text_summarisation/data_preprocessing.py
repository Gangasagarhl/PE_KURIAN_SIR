from langchain.text_splitter import RecursiveCharacterTextSplitter
import re
from collections import defaultdict


"""
In this what we do?? 
1. First group the data based on 5 minutes once then you can 

"""

class data_preprocessing: 
    @staticmethod
    def split_text(text, chunk_size=1900, overlap=50):
        """
        Split the text into chunks using LangChain's RecursiveCharacterTextSplitter.
        """
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
        return text_splitter.split_text(text)
    
    @staticmethod
    def convert_the_csv_to_text(csv):
        
        text =  ""
        col1,col2  = csv.columns[0],csv.columns[1]
        for _,col in csv.iterrows():
            #text += "   "+col[col1]
            text+= " "+ col[col2]
            
        text = data_preprocessing.split_text(text)
        return text
    

    
