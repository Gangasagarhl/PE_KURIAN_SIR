import cv2
import time
import os
from datetime import datetime
from image_descriptor import description

def main():
    # Define the folder to store captured images
    output_folder = "captured_images"
    os.makedirs(output_folder, exist_ok=True)

    # Open the default camera (device 0)
    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Error: Could not open the camera.")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Error: Failed to capture image.")
                break

            # Create a timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(output_folder, f"capture_{timestamp}.jpg")

            # Save the captured frame as a JPEG image
            cv2.imwrite(filename, frame)
            desc =description(frame)
            
            #this shall be sent t iitb server ip
            
            print(f"Saved image: {filename}")

            # Wait for 30 seconds before capturing the next image
            time.sleep(5)
    except KeyboardInterrupt:
        print("Terminated by user.")
    finally:
        cap.release()

if __name__ == "__main__":
    main()
