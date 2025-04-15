# server.py
from flask import Flask, request, jsonify
import csv
import os

# Import the models to ensure they are loaded
from model_manage import blip_model, blip_processor, t5_model, t5_tokenizer

# Import other modules (adjust paths as needed)
from analysis.donwload_video_from_client import video_photo_analyzer
from extreme_emergency_alerts.alert_neighbours import alert_neighbours

app = Flask(__name__)

CSV_FILE = "database/data.csv"

def initialize_csv():
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "description"])

initialize_csv()

@app.route("/upload", methods=["POST"])
def upload_data():
    data = request.get_json()
    if not data or "timestamp" not in data or "description" not in data:
        return jsonify({"status": "error", "message": "Missing required fields"}), 400

    timestamp = data["timestamp"]
    description = data["description"]
    print(f"[Upload] Received: {timestamp} - {description}")
    
    with open(CSV_FILE, "a", newline="", encoding="utf-8") as file:
        writer = csv.writer(file)
        writer.writerow([timestamp, description])
    
    return jsonify({"status": "success", "message": "Data received and saved"}), 200

# Create instances for video/photo analysis as needed.
va = video_photo_analyzer()
app.add_url_rule('/upload_video', view_func=va.upload_video, methods=['POST'])
app.add_url_rule('/upload_photo_for_summary', view_func=va.upload_photo, methods=['POST'])
app.add_url_rule('/emergency_alert_neighbours', view_func=alert_neighbours().truly_alert, methods=['POST'])

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
