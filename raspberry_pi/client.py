import cv2
import time
import threading
from datetime import datetime
import requests
#from image_descriptor import description  # BLIP model for image captioning
from models_inferences.keras_model_inference import  predict_image
from video_record_send_to_mail.index import execute_record
from send_emergency_video_to_sever_for_further_analysis.send_video_to_server import PassVideo
from datetime import datetime


# API Endpoints – adjust the host/port as needed.

ROOT = "http://127.0.0.1:5000"
IMAGE_UPLOAD_URL = ROOT+"/upload_photo"
VIDEO_UPLOAD_URL = ROOT+"/upload_video"


# Global variables for live streaming mode
live_streaming_mode = False
live_streaming_start_time = None
last_stream_sent_time = 0
stream_fps_interval = 0.1  # for ~10 fps streaming to the server


#this is used to send the descirtion to server
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



def capture_from_camera():
    global live_streaming_mode, live_streaming_start_time, last_stream_sent_time
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("Error: Could not open camera.")
        return

    capture_interval = 15
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
            inference_result = predict_image(frame)  # Perform model inference

            if inference_result == "BOTTLE":
                current_time = datetime.now()
                video_name =  f"recording_{current_time}.avi"

                print("Recording started for 15 seconds...")
                recording = True
                record_start_time = current_time
                # Set up the video writer
                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(f"send_emergency_video_to_sever_for_further_analysis/{video_name}", fourcc, fps, (frame_width, frame_height))

        else:
            # While recording, just write the frames without doing inference
            out.write(frame)
            # Check if 15 seconds have passed since recording started
            if current_time - record_start_time >= capture_interval:
                print("Recording stopped.")
                recording = False
                out.release()

                #this to be changed
                # Launch a thread to process/send the recorded video
                passvideo  = PassVideo( url= VIDEO_UPLOAD_URL, video_path = f"{video_name}", video_id="hlgsagar1")
                t1 = threading.Thread(target=passvideo.send)
                t1.start()
                
                # Optionally, update last_capture_time if you want to avoid immediate inference_worker trigger

        # Continue with periodic processing only if not recording
        if not recording and current_time - last_capture_time >= capture_interval:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            t2=threading.Thread(target=inference_worker, args=(frame.copy(), timestamp)).start()
            t2.start()
            last_capture_time = current_time

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()

    
   
if __name__ == "__main__":
    capture_from_camera()