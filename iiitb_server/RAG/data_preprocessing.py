import pandas as pd

class preprcoess:
    def __init__(self):
        print("preprocessing for the RAG")

    def execute(self):
        data = pd.read_csv("../database/data.csv")
        description = list(data['decsription'].values())
        data.iloc[0:0].to_csv("../database/data.csv", index=False)
        return description
    



