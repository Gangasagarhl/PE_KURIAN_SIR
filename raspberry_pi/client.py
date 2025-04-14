import cv2
import time
import threading
from datetime import datetime
import requests
#from image_descriptor import description  # BLIP model for image captioning
from models_inferences.keras_model_inference import  predict_image
#from video_record_send_to_mail.index import execute_record
from send_emergency_video_to_sever_for_further_analysis.send_video_to_server import PassVideo
from datetime import datetime



# API Endpoints – adjust the host/port as needed.
USER_ID = "sag1"
ADDRESS =  "VISVESVARAY@IIITB__\nHLG_SAGAR_\nPE_KURIAN_SIR"
ROOT = "http://127.0.0.1:5000"
IMAGE_UPLOAD_URL = ROOT+"/upload_photo_for_summary"
VIDEO_UPLOAD_URL = ROOT+"/upload_video"
EMERGENCY_CALL_NEIGHBOURS =  ROOT+"/emergency_alert_neighbours"


##this for making the emergeny alert to neightbours
FRAME_CHECKING = None
TOOK_FOR_TESTING = False  #if this is true thn it means then the thread is already created, which can be


# Global variables for live streaming mode
live_streaming_mode = False
live_streaming_start_time = None
last_stream_sent_time = 0
stream_fps_interval = 0.1  # for ~10 fps streaming to the server


#this is used to send the descirtion to server
def inference_worker(frame, timestamp):
    success, frame = cv2.imencode('.jpg', frame)
    files = {'image': (f'{timestamp}__{USER_ID}', frame.tobytes(), 'image/jpeg')}
    data={'id':USER_ID}
    response = requests.post(IMAGE_UPLOAD_URL, files=files,data=data)
    print("Image summariser response: ",response)



#used to call teh neighbours after some seconds   
def emergency_senders(video_name):
    time.sleep(60)
    global TOOK_FOR_TESTING,FRAME_CHECKING,EMERGENCY_CALL_NEIGHBOURS,USER_ID,ADDRESS
    TOOK_FOR_TESTING = False
    inference_result = predict_image(FRAME_CHECKING)
    
    if inference_result == "BOTTLE":
        PassVideo(url=EMERGENCY_CALL_NEIGHBOURS,video_path=video_name).send_emergency(id=USER_ID,address=ADDRESS)
        print("Bottle detected now called all teh neighbours\n")
        #call for sending alert to neightbours
        

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

            #this is used to check after 60 secs, if he bottle is seen then emergency true emergency
            global FRAME_CHECKING, TOOK_FOR_TESTING
            FRAME_CHECKING = frame
            if not TOOK_FOR_TESTING:
                TOOK_FOR_TESTING = True
                threading.Thread(target=emergency_senders,args=(video_name)).start()

            
            # Check if 15 seconds have passed since recording started
            if current_time - record_start_time >= capture_interval:
                print("Recording stopped.")
                recording = False
                out.release()

                #this to be changed
                # Launch a thread to process/send the recorded video
                passvideo  = PassVideo( url= VIDEO_UPLOAD_URL, video_path = f"{video_name}")
                t1 = threading.Thread(target=passvideo.send,args=(USER_ID))
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