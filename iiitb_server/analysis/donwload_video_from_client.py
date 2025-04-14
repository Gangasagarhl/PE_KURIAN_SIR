from flask import request, jsonify
import threading
import os
from analysis.index import make_it
import requests
import csv
import datetime
from analysis.image_descriptor import image_description
class video_photo_analyzer:

    def __init__(self,blip_model,blip_processor,t5_model,t5_tokenizer):
        self.blip_model=  blip_model
        self.blip_processor = blip_processor
        self.t5_model =  t5_model
        self.t5_tokenizer =  t5_tokenizer
        self.database = "../database"


    def upload_video(self):
        if 'video' not in request.files:
            return jsonify({'error': 'No video part in the request'}), 400

        video = request.files['video']

        if video.filename == '':
            return jsonify({'error': 'No selected video'}), 400

        # Save video
        save_path = os.path.join("videos", video.filename)
        video.save(save_path)

        print(f"✅ Received and saved video: {save_path}")

        # Call make_it which should return an object with send_to_recipients method
        result = make_it(save_path, output_folder="out",blip_model=self.blip_model, blip_processor=self.blip_processor, t5_model=self.t5_model, t5_tokenizer=self.t5_tokenizer)

        # Start send_to_recipients in a background thread
        print(" Threading to send notificatiosn\n")
        thread = threading.Thread(target=result.send_to_recepeints, args=("hlgsagar.2@gmail.com", 8105114611))
        thread.start()
        

        return jsonify({'message': 'Video uploaded successfully', 'filename': video.filename}), 200
    


    #this saves the description of the image that is passed to it in data.csv. 
    def save_the_description(self, photo_path,database_path,id):
        csv_path =  database_path+"/data.csv"
        file_exists = os.path.isfile(csv_path)
    
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'timestamp', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()  # Write header if file doesn't exist
            desc = image_description(self.blip_model,self.blip_processor)
            caption =  desc.description(photo_path)
            entry={
                'id':id,
                'timestamp':datetime.now(),
                'description': caption
                }
            writer.writerow(entry)

        os.remove(photo_path)
        
        


    def upload_photo(self):
    
        if 'image' not in request.files:
            return "No image part in the request", 400

        file = requests.files['image']
        id = requests.data['id']
        if file.filename == '':
            return "No selected file", 400

        # Save the file
        save_path = os.path.join("photo_temp",file.filename)
        file.save(save_path)

        t2= threading.Thread(self.save_the_description, args=(save_path,self.database,id))
        t2.start()

        return f"Image saved to {save_path}", 200
