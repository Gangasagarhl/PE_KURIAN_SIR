import requests
import os
import time
import threading
import mimetypes


class PassVideo: 
    def __init__(self, url, video_path, video_id=None):
        self.url = url
        self.video_path = video_path
        self.video_id = video_id

    def delete_video(self, video_path):
        time.sleep(600)
        try:
            os.remove(video_path)
            print(f"[INFO] Deleted: {video_path}")
        except Exception as e:
            print(f"[ERROR] Could not delete {video_path}: {e}")

    def send(self, user_id):
        print("\n[INFO] Sending normal video\n")
        if not os.path.exists(self.video_path):
            print(f"[ERROR] Video file not found: {self.video_path}")
            return

        # Extract file extension from the original video path.
        # For instance, if self.video_path is "videos/my_video.avi", then ext will be ".avi"
        _, ext = os.path.splitext(self.video_path)
        
        # Create a new filename using the user_id and the extension.
        # For example, if user_id is "sagar", the new filename will be "sagar.avi"
        new_filename = f"{user_id}{ext}"
        
        # Use mimetypes to guess the content type based on the new filename.
        mime_type, _ = mimetypes.guess_type(new_filename)
        if mime_type is None:
            mime_type = "application/octet-stream"
        
        with open(self.video_path, "rb") as f:
            # The tuple format here is (filename, file object, content type)
            files = {"video": (new_filename, f, mime_type)}
            data = {"id": user_id, "purpose": "LE"}
            
            try:
                response = requests.post(self.url, files=files, data=data)
                if response.status_code == 200:
                    print("[SUCCESS] Response:", response.json())
                    threading.Thread(target=self.delete_video, args=(self.video_path,)).start()
                else:
                    print(f"[ERROR] Server returned {response.status_code}")
                    print("Response:", response.text)
            except Exception as e:
                print("[ERROR] Failed to send video:", e)




    def send_emergency(self, id, address,url):
        print(f"\n[EMERGENCY] Preparing to send: {self.video_path}\n")
        if not os.path.exists(self.video_path):
            print(f"[ERROR] Video file not found: {self.video_path}")
            return

        with open(self.video_path, "rb") as f:
            print("get ready to send\n\n")
            files = {"video": f}
            data = {"id": id, "address": address}

            print("\nEmergency URL: ", url)

            try:
                response = requests.post(url, files=files, data=data)
                if response.status_code == 200:
                    print("[SUCCESS] Emergency video sent:", response.json())
                else:
                    print(f"[ERROR] Server returned {response.status_code}")
                    print("Response:", response.text)
            except Exception as e:
                print("[ERROR] Failed to send emergency video:", e)

    
