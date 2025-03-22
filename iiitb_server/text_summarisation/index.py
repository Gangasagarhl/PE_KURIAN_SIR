"""
The steps are very simple
0. load the model and token from the saved model, passit to the summary. 
1. Get the data from database
2. post that data to the data preprocessing
3. generate the summary
4. store the summary to the database.
"""

from load_model import model_load
from data_loading import extract_csv_data
from data_preprocessing import data_preprocessing
from generate_summary import GenerateSummary
from send_mail import send_mail

def execute_program():
    
    #token, model load from from the model object.
    #model_obj =  model_load()
    #tokenizer, model = model_obj.model_load()
    print("Model loading is done:\n\n")
    
    #get the data from database
    path="../database/data.csv"
    data_obj =  extract_csv_data()
    data =  data_obj.extract_total(path)
    print("got data from database\n\n")
    #print("***********************\n\nData:  \n", data,"\n\n\n\n")
    
    #data preprocessing
    pre_obj = data_preprocessing()
    chunks =  pre_obj.convert_the_csv_to_text(data)
    print("Data preprocessing is done\n\n")
    print("\n\n\nChunks Length: ", len(chunks), "\n")
    
    
    ##generate the summary
    summary_obj =  GenerateSummary()
    summary =  summary_obj.refine_summarization(chunks)
    send_mail(summary)
    
    print("Summary from the data recieved:  ",  summary)
    

if __name__ == "__main__":
    execute_program()

