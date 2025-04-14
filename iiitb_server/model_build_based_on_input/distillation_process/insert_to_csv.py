import csv
import os
import cv2
from image_descriptor import description
#from insert_to_csv import insert_sentences_into_csv

def insert_sentences_into_csv(sentence1, sentence2, csv_file_path):
    """
    Inserts two sentences into a CSV file as a new row with two columns.
    
    Args:
        sentence1 (str): Text for the first column.
        sentence2 (str): Text for the second column.
        csv_file_path (str): The file path to the CSV file.
    """
    # Check if the CSV file already exists
    file_exists = os.path.isfile(csv_file_path)
    
    # Open the file in append mode
    with open(csv_file_path, mode='a', newline='', encoding='utf-8') as csv_file:
        # Define the column names
        fieldnames = ['image', 'caption']
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        
        # If the file does not exist, write the header first
        if not file_exists:
            writer.writeheader()
        
        # Write the new row with the provided sentences
        writer.writerow({'image': sentence1, 'caption': sentence2})


def read_image_pass_for_description(path):
    img = cv2.imread(path)
    caption = description(img)
    insert_sentences_into_csv(path, caption,"data.csv")
    






# Example usage:
if __name__ == "__main__":

    for i in os.listdir("out/"):
       full_path = os.path.join("out", i)
       read_image_pass_for_description(full_path)
