import requests
import os
import time
import threading

class PassVideo: 
    def __init__(self, url, video_path, video_id=None):
        self.url = url
        self.video_path = video_path
        self.video_id = video_id  # Add optional ID support

    def delete_video(self,video_path):
        time.sleep(100)
        os.remove(video_path)
        print(f"Deleted: {self.video_path}")
    

    def send(self,user_id):
        with open(self.video_path, "rb") as f:
            files = {"video": f}
            data = {"id": user_id} 

            try:
                response = requests.post(self.url, files=files, data=data)
                
                if response.status_code == 200:
                    print("Response:", response.json())
                    threading.Thread(target=self.delete_video, args=(self.video_path)).start()
                    
                else:
                    print(f"Server returned status {response.status_code}")
                    print("Response:", response.text)
            except Exception as e:
                print("Failed to parse JSON response:", e)
                print("Raw Response Text:", response.text)



    def send_emergency(self,id,address):
        with open(self.video_path, "rb") as f:
            files = {"video": f}
            data = {"id": id,"address":address} 

            try:
                response = requests.post(self.url, files=files, data=data)
                
                if response.status_code == 200:
                    print("Response:", response.json())
                    
                else:
                    print(f"Server returned status {response.status_code}")
                    print("Response:", response.text)
            except Exception as e:
                print("Failed to parse JSON response:", e)
                print("Raw Response Text:", response.text)


