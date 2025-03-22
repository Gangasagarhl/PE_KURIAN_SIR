from flask import Flask, request, jsonify, Response, render_template_string
import numpy as np
import cv2
import time
import threading
from datetime import datetime
import csv
import os

app = Flask(__name__)

# --- LiveSession Implementation ---
class LiveSession:
    def __init__(self):
        self.active = False
        self.start_time = None
        self.latest_frame = None
        self.video_writer = None
        self.last_record_time = None
        self.recording_lock = threading.Lock()

    def start(self, frame):
        with self.recording_lock:
            self.active = True
            self.start_time = time.time()
            self.latest_frame = frame
            self.last_record_time = time.time()
            h, w, _ = frame.shape
            filename = datetime.now().strftime("live_%Y%m%d_%H%M%S.avi")
            fourcc = cv2.VideoWriter_fourcc(*'XVID')
            self.video_writer = cv2.VideoWriter(filename, fourcc, 10, (w, h))
            print(f"Live session started. Saving video to {filename}")

    def update(self, frame):
        with self.recording_lock:
            self.latest_frame = frame
            current_time = time.time()
            # Write frame if at least 1/10 sec has passed.
            if current_time - self.last_record_time >= 0.1:
                if self.video_writer is not None:
                    self.video_writer.write(frame)
                self.last_record_time = current_time
            # Automatically end session after 5 minutes.
            if current_time - self.start_time > 300:
                self.end()

    def get_latest_frame(self):
        with self.recording_lock:
            return self.latest_frame

    def end(self):
        with self.recording_lock:
            self.active = False
            if self.video_writer is not None:
                self.video_writer.release()
                self.video_writer = None
            print("Live session ended and video saved.")

# Global live session instance.
live_session = LiveSession()

"""
# --- Endpoints ---
@app.route('/upload', methods=['POST'])
def upload_data():
    data = request.get_json()
    if not data:
        return jsonify({"status": "error", "message": "No JSON data received"}), 400

    timestamp = data.get("timestamp")
    description = data.get("description")
    if not timestamp or not description:
        return jsonify({"status": "error", "message": "Missing timestamp or description"}), 400

    print(f"[Upload] Received: {timestamp} - {description}")
    # (Assume CSV logging is handled elsewhere.)
    return jsonify({"status": "success", "message": "Data received"}), 200"
"""



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









@app.route('/live_video', methods=['POST'])
def live_video():
    if 'frame' not in request.files:
        return jsonify({"status": "error", "message": "No frame received"}), 400

    frame_data = request.files['frame'].read()
    np_arr = np.frombuffer(frame_data, np.uint8)
    frame = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    if frame is None:
        return jsonify({"status": "error", "message": "Failed to decode frame"}), 400

    if not live_session.active:
        live_session.start(frame)
    live_session.update(frame)
    return jsonify({"status": "success", "message": "Frame received"}), 200

@app.route('/stream_control', methods=['GET'])
def stream_control():
    return jsonify({"active": live_session.active})

@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    if live_session.active:
        live_session.end()
        return jsonify({"status": "success", "message": "Live streaming stopped"}), 200
    return jsonify({"status": "error", "message": "No active live session"}), 400

@app.route('/control', methods=['GET'])
def control_page():
    return render_template_string('''
        <html>
        <head>
            <title>Live Stream Control</title>
        </head>
        <body>
            <h1>Live Stream</h1>
            <img src="{{ url_for('video_feed') }}" width="640" height="480">
            <form action="{{ url_for('stop_stream') }}" method="post">
                <button type="submit">Stop Live Streaming</button>
            </form>
        </body>
        </html>
    ''')

def generate_frames():
    last_yield_time = 0
    while True:
        if live_session.active and live_session.get_latest_frame() is not None:
            current_time = time.time()
            # Stream one frame every 5 seconds.
            if current_time - last_yield_time >= 5:
                last_yield_time = current_time
                frame = live_session.get_latest_frame()
                ret, buffer = cv2.imencode('.jpg', frame)
                if ret:
                    frame_bytes = buffer.tobytes()
                    yield (b'--frame\r\n'
                           b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            # If no active live session, yield a blank frame.
            blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            ret, buffer = cv2.imencode('.jpg', blank_frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
            time.sleep(5)

@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
