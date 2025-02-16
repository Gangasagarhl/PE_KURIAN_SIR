import cv2
import time
import requests
import threading

def stream_frame(frame, live_stream_url):
    """
    Encode a frame as JPEG and send it to the live streaming endpoint.
    """
    ret, jpeg = cv2.imencode('.jpg', frame)
    if not ret:
        print("Error: Could not encode frame.")
        return
    files = {'frame': ('frame.jpg', jpeg.tobytes(), 'image/jpeg')}
    try:
        # POST the frame (timeout set to avoid blocking)
        requests.post(live_stream_url, files=files, timeout=1)
    except Exception as e:
        print("Error streaming frame:", e)

def start_live_video_call(cap, live_stream_url, duration=120, fps=10):
    """
    Streams frames from the camera to the server for the given duration.
    - cap: OpenCV VideoCapture object.
    - live_stream_url: URL of the server’s live video endpoint.
    - duration: Streaming duration in seconds (default is 120 seconds).
    - fps: Frames per second for streaming.
    """
    end_time = time.time() + duration
    interval = 1.0 / fps
    while time.time() < end_time:
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture frame for live streaming.")
            break
        # Send each frame in a separate thread to avoid blocking the capture loop
        threading.Thread(target=stream_frame, args=(frame, live_stream_url)).start()
        time.sleep(interval)
    print("Live video streaming ended.")
