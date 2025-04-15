import os
import cv2
import time
import threading
from datetime import datetime
import requests
from models_inferences.keras_model_inference import predict_image
from send_emergency_video_to_sever_for_further_analysis.send_video_to_server import PassVideo

# API Endpoints – adjust the host/port as needed.

USER_ID = "sag1"
ADDRESS = "VISVESVARAY@IIITB__\nHLG_SAGAR_\nPE_KURIAN_SIR"
ROOT = "http://127.0.0.1:5000"
IMAGE_UPLOAD_URL = ROOT + "/upload_photo_for_summary"
VIDEO_UPLOAD_URL = ROOT + "/upload_video"
EMERGENCY_CALL_NEIGHBOURS = ROOT + "/emergency_alert_neighbours"
COUNT_FOR_EMERGENCY = 0 #if more than 3 times it is counted in 
#2 minutes then it will trigger the emergency
CURRENT_EMERGENCY_TIME=0
EMERGENCY_VIDEO_PATH = None

# Globals
FRAME_CHECKING = None
TOOK_FOR_TESTING = False
capture_interval = 15  # seconds
fps = 20

# Video output directory
video_output_dir = "send_emergency_video_to_sever_for_further_analysis"
os.makedirs(video_output_dir, exist_ok=True)



##the image is sent to the server for making the summarisation



def inference_worker(frame, timestamp):
    success, frame_encoded = cv2.imencode('.jpg', frame)
    if not success:
        print("[ERROR] Frame encoding failed.")
        return

    files = {'image': (f'{timestamp}__{USER_ID}.jpg', frame_encoded.tobytes(), 'image/jpeg')}
    data = {'id': USER_ID}

    try:
        response = requests.post(IMAGE_UPLOAD_URL, files=files, data=data)
        print("[INFO] Image summary response:", response.status_code, response.text)
    except Exception as e:
        print("[ERROR] Failed to send image:", e)



    
"""
def emergency_senders(video_path):
    print("\n\n\n\n******************emergencyyyyyyyy****************\n\n")
    PassVideo(url=EMERGENCY_CALL_NEIGHBOURS, video_path=video_path).send_emergency(id=USER_ID, address=ADDRESS)
    print("[ALERT] BOTTLE detected – Emergency alert sent to neighbours.")
"""
    
def emergency_senders(video_path):
    #print("\n********** EMERGENCY ALERT **********\n\n\n")
    #rint("\n********** EMERGENCY ALERT **********\n")

    PassVideo(url=EMERGENCY_CALL_NEIGHBOURS, video_path=video_path).send_emergency(
        id=USER_ID, address=ADDRESS,url=EMERGENCY_CALL_NEIGHBOURS
    )
    print("[ALERT] BOTTLE detected – Emergency alert sent to neighbours.")

    
        

def capture_from_camera():
    global FRAME_CHECKING, TOOK_FOR_TESTING

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("[ERROR] Could not open camera.")
        return

    last_capture_time = time.time()
    recording = False
    record_start_time = None
    out = None

    frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    print("[INFO] Camera started successfully...")
    
    bottle_count = 0
    bottle_time_marked = None
    emergency_video_path = None
    

    while True:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture frame.")
            break

        current_time = time.time()

        # Display red "REC" text if recording
        if recording:
            cv2.putText(frame, "REC", (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 0, 255), 3)

        # Show the frame
        cv2.imshow("Live Camera Feed", frame)

        if not recording:
            result = predict_image(frame)


            if result == "BOTTLE":
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                video_name = f"recording_{timestamp}.avi"
                video_path = os.path.join(video_output_dir, video_name)

                print("[INFO] BOTTLE detected – starting recording...")
                recording = True
                record_start_time = current_time

                if bottle_count<=0:
                    emergency_video_path = video_path
                    bottle_time_marked =  time.time()
                    print("Bottle marked at 0: ",bottle_time_marked,"\nvideo path: ", video_path)
                

                if bottle_count > 4:
                    elapsed =  int(time.time() - bottle_time_marked)
                    print("elapsed time\n",elapsed)

                    if elapsed < 300:
                        print("\n\nEmergency vidoe path: ", emergency_video_path)
                        emergency_senders(emergency_video_path)
                        elapsed=0

                    bottle_count = -1
                    
                bottle_count+=1
                print("\n\nBottle count:  ",bottle_count)
                elapsed =  int(time.time() - bottle_time_marked)
                print("elapsed time\n",elapsed)

                fourcc = cv2.VideoWriter_fourcc(*'XVID')
                out = cv2.VideoWriter(video_path, fourcc, fps, (frame_width, frame_height))
        else:
            out.write(frame)

            if current_time - record_start_time >= capture_interval:
                print("[INFO] Recording complete.")
                recording = False
                out.release()

                video_path = os.path.join(video_output_dir, video_name)
                threading.Thread(
                    target=PassVideo(url=VIDEO_UPLOAD_URL, video_path=video_path).send,
                    args=(USER_ID,)
                ).start()

        if not recording and current_time - last_capture_time >= capture_interval:
            timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
            threading.Thread(target=inference_worker, args=(frame.copy(), timestamp)).start()
            last_capture_time = current_time

        # Press 'q' to quit the feed
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] 'q' pressed – Exiting camera feed.")
            break

        time.sleep(0.01)

    cap.release()
    cv2.destroyAllWindows()
    print("[INFO] Camera and windows released.")



def check_by_calling_emergency():
    video_output_dir = "send_emergency_video_to_sever_for_further_analysis"
    video_path = "recording_20250415_042426.avi"
    video_path = os.path.join(video_output_dir,video_path)
    threading.Thread(target=emergency_senders,args=(video_path,)).start()
    



if __name__ == "__main__":
    capture_from_camera()