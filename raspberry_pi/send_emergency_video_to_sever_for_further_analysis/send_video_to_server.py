import requests
import os

class PassVideo: 
    def __init__(self, url, video_path, video_id=None):
        self.url = url
        self.video_path = video_path
        self.video_id = video_id  # Add optional ID support

    def send(self):
        with open(self.video_path, "rb") as f:
            files = {"video": f}
            data = {"id": self.video_id} if self.video_id else {}

            try:
                response = requests.post(self.url, files=files, data=data)
                
                if response.status_code == 200:
                    print("Response:", response.json())
                    os.remove(self.video_path)
                    print(f"Deleted: {self.video_path}")
                else:
                    print(f"Server returned status {response.status_code}")
                    print("Response:", response.text)
            except Exception as e:
                print("Failed to parse JSON response:", e)
                print("Raw Response Text:", response.text)
