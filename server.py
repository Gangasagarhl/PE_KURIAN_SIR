from flask import Flask, request, jsonify
from flask_socketio import SocketIO, disconnect
import csv
import os


# Load models
#from iiitb_server.model_manage import blip_model, blip_processor, t5_model, t5_tokenizer
#hold the name of the resource
from iiitb_server.resource_allocation_disallocation import resource_holder

# Load modules
from iiitb_server.analysis.donwload_video_from_client import video_photo_analyzer
from iiitb_server.extreme_emergency_alerts.alert_neighbours import alert_neighbours

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'  # Needed for socketio
socketio = SocketIO(app, cors_allowed_origins="*")  # Enable CORS for testing

CSV_FILE = "iiitb_server/database/data.csv"

def initialize_csv():
    os.makedirs(os.path.dirname(CSV_FILE), exist_ok=True)
    if not os.path.exists(CSV_FILE):
        with open(CSV_FILE, "w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["timestamp", "description"])

initialize_csv()



# 🔁 Add URL rules

va =  video_photo_analyzer()

app.add_url_rule('/upload_video', view_func=va.upload_video, methods=['POST'])
app.add_url_rule('/upload_photo_for_summary', view_func=va.upload_photo, methods=['POST'])
app.add_url_rule('/emergency_alert_neighbours', view_func=alert_neighbours().truly_alert, methods=['POST'])




# 🔌 SocketIO Events
@socketio.on('connect')
def handle_connect():
    print(f"🔌 Client connected: {request.sid}")

@socketio.on('disconnect')
def handle_disconnect():
    print(f"❌ Client disconnected: {request.sid}")
    try:
        os.remove("iiitb_server/analysis/videos/sag1_LE_sag1.avi")
        print("file deleted after disconnecting\n")
    except:
        print("file is not available\n")





if __name__ == "__main__":
    socketio.run(app, host='0.0.0.0', port=5000, debug=True)









