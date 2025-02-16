from flask import Flask, request, jsonify, Response, render_template_string
import numpy as np
import cv2
import time
from csv_handler import init_csv, append_to_csv
from live_session import LiveSession

app = Flask(__name__)
init_csv()  # Ensure CSV file exists

# Global live session instance
live_session = LiveSession()



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
    try:
        append_to_csv(timestamp, description)
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

    return jsonify({"status": "success", "message": "Data received"}), 200






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
    """Return whether live streaming is active."""
    return jsonify({"active": live_session.active})




@app.route('/stop_stream', methods=['POST'])
def stop_stream():
    if live_session.active:
        live_session.end()
        return jsonify({"status": "success", "message": "Live streaming stopped"}), 200
    return jsonify({"status": "error", "message": "No active live session"}), 400







@app.route('/control', methods=['GET'])
def control_page():
    """A simple control page with the live feed and a Stop button."""
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
    """Generator that yields MJPEG frames for the video feed."""
    while True:
        if live_session.active and live_session.get_latest_frame() is not None:
            frame = live_session.get_latest_frame()
            ret, buffer = cv2.imencode('.jpg', frame)
            if ret:
                frame_bytes = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        else:
            # Yield a blank frame if no active live session
            blank_frame = np.zeros((480, 640, 3), dtype=np.uint8)
            ret, buffer = cv2.imencode('.jpg', blank_frame)
            frame_bytes = buffer.tobytes()
            yield (b'--frame\r\n'
                   b'Content-Type: image/jpeg\r\n\r\n' + frame_bytes + b'\r\n')
        time.sleep(0.03)






@app.route('/video_feed')
def video_feed():
    return Response(generate_frames(), mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
