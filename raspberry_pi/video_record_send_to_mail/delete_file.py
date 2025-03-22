import os

def delete_file(file_path="video_record_send_to_mail/recording.avi"):
    
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"{file_path} deleted successfully.")
        else:
            print(f"{file_path} does not exist.")
    except Exception as e:
        print(f"Error: {e}")


