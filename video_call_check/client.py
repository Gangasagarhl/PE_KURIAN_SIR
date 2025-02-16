# client.py
import cv2
import requests
import time

SERVER_UPLOAD_URL = "http://127.0.0.1:5000/upload_frame"

def stream_video():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open video capture")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            # Encode the frame as JPEG
            ret, buffer = cv2.imencode('.jpg', frame)
            if not ret:
                print("Failed to encode frame")
                continue

            files = {'frame': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
            try:
                response = requests.post(SERVER_UPLOAD_URL, files=files, timeout=1)
                if response.status_code != 200:
                    print("Server response:", response.text)
                    # Break out of the loop if the server stops streaming
                    break
            except requests.exceptions.RequestException as e:
                print("Request exception:", e)
                break

            # Show the video locally (optional)
            cv2.imshow("Client - Streaming", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

            time.sleep(0.05)  # Adjust for approximate 20 FPS
    finally:
        cap.release()
        cv2.destroyAllWindows()

if __name__ == '__main__':
    stream_video()
