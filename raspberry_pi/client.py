import cv2
import time
import threading
from datetime import datetime
import requests
from image_descriptor import description  # BLIP model for image captioning
from whatsapp_alert import send_whatsapp_alert
from model_inference import Inference
from video_record_send_to_mail.index import execute_record

inference=Inference()#This is used for continous monitoring of the data frames using mobilenet model

# API Endpoints – adjust the host/port as needed.
IMAGE_UPLOAD_URL = "http://127.0.0.1:5000/upload"


# Global variables for live streaming mode
live_streaming_mode = False
live_streaming_start_time = None
last_stream_sent_time = 0
stream_fps_interval = 0.1  # for ~10 fps streaming to the server

def send_frame_to_server(frame):
    try:
        _, buffer = cv2.imencode('.jpg', frame)
        files = {'frame': ('frame.jpg', buffer.tobytes(), 'image/jpeg')}
        # Use a short timeout so sending does not block the main loop.
        requests.post(LIVE_VIDEO_URL, files=files, timeout=1)
    except Exception as e:
        print("Error sending live stream frame:", e)



def inference_worker(frame, timestamp):
    global live_streaming_mode, live_streaming_start_time
    start_time = datetime.now()
    caption = description(frame)
    
    latency = datetime.now() - start_time
    cv2.imwrite("captured_images/"+str(datetime.now())+"_output.jpg",frame)
    
    print("Inference latency:", latency)
    print(f"[Captured] {timestamp} - Description: {caption}\n\n")

    # Send the description to the server.
    payload = {"timestamp": timestamp, "description": caption}
    try:
        requests.post(IMAGE_UPLOAD_URL, json=payload)
    except Exception as e:
        print("Error sending data:", e)
    '''
    # If the description contains "leopard" or "gun", trigger alert and live streaming.
    if "leopard" in caption.lower() or "gun" in caption.lower():
        control_link = "https://1e31-103-156-19-229.ngrok-free.app/live_video"  # update as needed
        alert_message = f"Alert: {caption} detected at {timestamp}.\nView live stream: {control_link}"
        try:
            sid = send_whatsapp_alert(alert_message)
            print("WhatsApp alert sent, SID:", sid)
        except Exception as e:
            print("Error sending WhatsApp alert:", e)
        # Activate live streaming mode if not already active.
        if not live_streaming_mode:
            live_streaming_mode = True
            live_streaming_start_time = time.time()
            print("Live streaming mode activated.")
            
        '''

def capture_from_video(video_path):
    global live_streaming_mode, live_streaming_start_time, last_stream_sent_time
    cap = cv2.VideoCapture(video_path)
    if not cap.isOpened():
        print("Error: Could not open video file.")
        return

    fps = cap.get(cv2.CAP_PROP_FPS)
    if fps <= 0:
        fps = 25
    delay = int(1000 / fps)

    capture_interval = 10  # seconds: capture frame for inference every 15 sec.
    last_capture_time = time.time()

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        # Show video normally.
        cv2.imshow("Video Feed", frame)
        current_time = time.time()

        # Trigger asynchronous inference every 15 seconds.
        if current_time - last_capture_time >= capture_interval:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            threading.Thread(target=inference_worker, args=(frame.copy(), timestamp)).start()
            last_capture_time = current_time

        # If live streaming mode is active, send frames to the server at ~10 fps.
        if live_streaming_mode:
            if current_time - live_streaming_start_time > 300:  # 5 minutes = 300 sec.
                live_streaming_mode = False
                print("Live streaming mode deactivated after 5 minutes.")
            else:
                if current_time - last_stream_sent_time >= stream_fps_interval:
                    send_frame_to_server(frame)
                    last_stream_sent_time = current_time

        if cv2.waitKey(delay) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()














import time

def capture_from_camera():
    global live_streaming_mode, live_streaming_start_time, last_stream_sent_time
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    capture_interval = 10
    last_capture_time = time.time()
    
    # Parameters for recording
    recording = False
    record_start_time = None
    fps = 20  # Frames per second
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = None

    while True:
        ret_frame, frame = cap.read()
        if not ret_frame:
            print("Error capturing frame")
            break

        cv2.imshow("Live Camera", frame)
        current_time = time.time()

        if not recording:
            # Only perform inference if not currently recording
            inference_result = inference.inference(frame)  # Perform model inference

            if inference_result == "record":
                print("Recording started for 10 seconds...")
                recording = True
                record_start_time = current_time
                # Set up the video writer
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter("video_record_send_to_mail/recording.avi", fourcc, fps, (frame_width, frame_height))
        else:
            # While recording, just write the frames without doing inference
            out.write(frame)
            # Check if 10 seconds have passed since recording started
            if current_time - record_start_time >= 10:
                print("Recording stopped.")
                recording = False
                out.release()
                # Launch a thread to process/send the recorded video
                t1 = threading.Thread(target=execute_record, args=("hlgsagar.2@gmail.com",))
                t1.start()
                
                # Optionally, update last_capture_time if you want to avoid immediate inference_worker trigger

        # Continue with periodic processing only if not recording
        if not recording and current_time - last_capture_time >= capture_interval:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            threading.Thread(target=inference_worker, args=(frame.copy(), timestamp)).start()
            last_capture_time = current_time

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    





def main():
    choice = input("Choose source: (1) Video file (2) Live Camera: ").strip()
    if choice == "1":
        video_path = input("Enter video file path: ").strip()
        capture_from_video(video_path)
    elif choice == "2":
        capture_from_camera()
    else:
        print("Invalid choice. Exiting.")

if __name__ == "__main__":
    main()
