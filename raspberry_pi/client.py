import cv2
import time
from datetime import datetime
import requests
from image_descriptor import description  # Your module to produce an image description
from whatsapp_alert import send_whatsapp_alert

# Endpoints (update IP/port as needed)
IMAGE_UPLOAD_URL = "http://127.0.0.1:5000/upload"
LIVE_VIDEO_URL   = "http://127.0.0.1:5000/live_video"
STREAM_CTRL_URL  = "http://127.0.0.1:5000/stream_control"


def check_live_stream_status():
    """Polls the server to check if live streaming is still active."""
    try:
        response = requests.get(STREAM_CTRL_URL)
        if response.status_code == 200:
            data = response.json()
            return data.get("active", False)
    except Exception as e:
        print("Error checking live stream status:", e)
    return False


def main():
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    live_streaming = False

    try:
        while True:
            
            ret, frame = cap.read()
            if not ret:
                print("Error capturing frame")
                break

            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            desc = description(frame)
            print(f"[Normal] {timestamp} - Description: {desc}")

            # Send normal image data to the server
            payload = {"timestamp": timestamp, "description": desc}
            try:
                r = requests.post(IMAGE_UPLOAD_URL, json=payload)
                print("[Upload]", r.status_code)
            except Exception as e:
                print("Error sending data:", e)

            # If alert condition is met and not already streaming...
            if (("leopard" in desc.lower() or "gun" in desc.lower()) and not live_streaming):
                # Send WhatsApp alert with a link to the control page
                
                control_link = "https://bfc0-103-156-19-229.ngrok-free.app/control"  # Update with your server address
                alert_message = f"Alert: {desc} detected at {timestamp}.\nView live stream: {control_link}"
                
                
                try:
                    sid = send_whatsapp_alert(alert_message)
                    print("WhatsApp alert sent, SID:", sid)
                except Exception as e:
                    print("Error sending WhatsApp alert:", e)

                live_streaming = True
                print("Switching to live streaming mode.")



            # If live streaming mode is active, send live frames and poll status
            if live_streaming:
                ret, frame = cap.read()
                if ret:
                    ret_enc, buffer = cv2.imencode('.jpg', frame)
                    if ret_enc:
                        files = {"frame": ("frame.jpg", buffer.tobytes(), "image/jpeg")}
                        try:
                            r = requests.post(LIVE_VIDEO_URL, files=files)
                        except Exception as e:
                            print("Error sending live frame:", e)
                # Poll server to see if live streaming should continue
                if not check_live_stream_status():
                    print("Live streaming stopped by user control.")
                    live_streaming = False

                # When live streaming, poll frames more frequently
                time.sleep(1)
            else:
                #the number is in seconds
                time.sleep(1)
    except KeyboardInterrupt:
        print("Terminated by user.")
    finally:
        cap.release()

if __name__ == "__main__":
    main()
