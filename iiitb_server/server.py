from flask import Flask, request, jsonify, Response, render_template_string
import numpy as np
import cv2
import time
import threading
from datetime import datetime
import csv
import os
from transformers import BlipProcessor, BlipForConditionalGeneration,T5Tokenizer, T5ForConditionalGeneration
from analysis.donwload_video_from_client import video_photo_analyzer
from extreme_emergency_alerts import alert_neighbours
app = Flask(__name__)


class blip_load:
    def __init__(self):
        self.loaded = False  # Flag to track loading status
        print("⏳ Loading BLIP model...")

        model_name = "Salesforce/blip-image-captioning-base"
        self.processor = BlipProcessor.from_pretrained(model_name)
        self.model = BlipForConditionalGeneration.from_pretrained(model_name)

        self.loaded = True
        print("\n✅✅✅ BLIP MODEL LOADED SUCCESSFULLY ✅✅✅\n")

    def is_ready(self):
        return self.model,self.processor
    

class t5_load:
    def __init__(self):
        model_name = "t5-base"
        self.tokenizer = T5Tokenizer.from_pretrained(model_name)
        self.model = T5ForConditionalGeneration.from_pretrained(model_name)
        print("\n\n*********T5 MODEL DOWNLOADED*********\n\n")
        
        self.loaded = True
        print("\n✅✅✅ t5 MODEL LOADED SUCCESSFULLY ✅✅✅\n")

    def is_ready(self):
        return self.model, self.tokenizer


blip = blip_load()
t5 =t5_load()

blip_model,blip_processor =  blip.is_ready()
t5_model,t5_tokenizer =  t5.is_ready()



CSV_FILE = "database/data.csv"

# Ensure CSV file and directory exist
def initialize_csv():
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)  # Ensure directory exists
    file_exists = os.path.exists(CSV_FILE)

    if not file_exists:
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "description"])  # Write header only if file is new

initialize_csv()

@app.route("/upload", methods=["POST"])
def upload_data():
    data = request.get_json()
    
    if not data or "timestamp" not in data or "description" not in data:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    timestamp = data["timestamp"]
    description = data["description"]

    print(f"[Upload] Received: {timestamp} - {description}")
    
    # Append data to CSV file
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, description])
    
    return jsonify({"status": "success", "message": "Data received and saved"}), 200


#this uploads video here and based on this, further analysis will be done
va = video_photo_analyzer(blip_model, blip_processor, t5_model, t5_tokenizer )
app.add_url_rule('/upload_video', view_func=va.upload_video, methods=['POST'])
app.add_url_rule('/upload_photo', view_func=va.upload_photo, methods=['POST'])

app.add_url_rule('/emergency_alert_neighbours',view_func =  emergency_alert,methods=['POST'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5001, debug=True)
