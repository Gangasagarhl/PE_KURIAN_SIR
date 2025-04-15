from flask import request, jsonify
import threading
import os
import csv
import datetime
from analysis.index import make_it
from analysis.image_descriptor import ImageDescription
global blip_model, blip_processor, t5_model, t5_tokenizer
class video_photo_analyzer:
    def __init__(self, ):
        
        self.database = "database"
        self.photo_temp_dir = "photo_temp"
        self.video_dir = "videos"

        os.makedirs(self.database, exist_ok=True)
        os.makedirs(self.photo_temp_dir, exist_ok=True)
        os.makedirs(self.video_dir, exist_ok=True)






    def upload_video(self):
        if 'video' not in request.files:
            return jsonify({'error': 'No video part in the request'}), 400

        video = request.files['video']
        id = request.form.get('id')
        purpose = request.form.get('purpose')
        print("Purpose: ", purpose)
        if video.filename == '':
            return "No selected video", 400

        
        new_filename = f"{id}_{purpose}_{video.filename}"
        save_path = os.path.join(self.video_dir, new_filename)
        print("save path: ", save_path)
        

        if not os.path.isfile(save_path):
            video.save(save_path)
            print(f"✅ Received and saved video: {save_path}")

            result = make_it(
                save_path,
                output_folder="out",
            )

            print("🔄 Starting thread to send notifications...")
            thread = threading.Thread(
                target=result.send_to_recepeints,
                args=("hlgsagar.2@gmail.com", 8105114611)
            )
            thread.start()

        return jsonify({'message': 'Video uploaded successfully', 'filename': video.filename}), 200







    def save_the_description(self, photo_path, database_path, id):
        csv_path = os.path.join(database_path, "data.csv")
        file_exists = os.path.isfile(csv_path)

        desc = ImageDescription()
        caption = desc.description(photo_path)

        # Ensure timestamp is string
        timestamp_str = datetime.datetime.now().isoformat()

        # Ensure correct field names
        entry = {
            'id': id,
            'timestamp': timestamp_str,
            'description': caption
        }

        # Safely write to CSV
        with open(csv_path, 'a', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['id', 'timestamp', 'description']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            if not file_exists:
                writer.writeheader()  # Write header once

            # Write only allowed keys
            clean_entry = {key: entry[key] for key in fieldnames}
            writer.writerow(clean_entry)

        # Cleanup photo
        os.remove(photo_path)



    def upload_photo(self):
        print("\n[INFO] Receiving photo...\n")
        if 'image' not in request.files:
            return "No image part in the request", 400

        file = request.files['image']
        id = request.form.get('id')

        if file.filename == '':
            return "No selected file", 400

        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        save_filename = f"{timestamp}__{id}.jpg"
        save_path = os.path.join(self.photo_temp_dir, save_filename)

        print(f"[INFO] Saving photo to: {save_path}")
        file.save(save_path)

        print("[INFO] Starting thread for image description...")
        t2 = threading.Thread(target=self.save_the_description, args=(save_path, self.database, id))
        t2.start()

        return f"Image saved and processing started: {save_path}", 200
