# analysis/image_descriptor.py
import os
import cv2
import warnings
from PIL import Image  # PIL for image loading
warnings.filterwarnings("ignore")

# Import the globally loaded models from model_manager
from iiitb_server.model_manage import blip_model, blip_processor

class ImageDescription:
    def __init__(self):
        print("\n\n*********IMAGE DESCRIPTION*********\n\n")

    def description(self, image_path):
        # Load the image from the provided file path
        image = Image.open(image_path).convert("RGB")
        # Use the globally loaded BLIP processor and model to generate a caption
        inputs = blip_processor(images=image, return_tensors="pt")
        output = blip_model.generate(**inputs)
        caption = blip_processor.decode(output[0], skip_special_tokens=True)
        return caption



class GetCaptions:
    def __init__(self):
        self.describer = ImageDescription()
        self.captions_list = []

    def extract_images_from_video_returns_list_of_captions(self, video_path, output_folder, fps_extract=1):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)
        print("Extracting the image from the video\n")

        cap = cv2.VideoCapture(video_path)
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / video_fps

        print(f"🎥 Video loaded. Duration: {duration:.2f}s, FPS: {video_fps}")

        second = 0
        current_time = 0.0

        while current_time < duration:
            print(f"\n🕒 Processing second: {second}")
            for i in range(fps_extract):
                timestamp = second + (i / fps_extract)
                cap.set(cv2.CAP_PROP_POS_MSEC, timestamp * 1000)
                success, frame = cap.read()

                if not success:
                    print(f"❌ Failed to extract frame at {timestamp:.2f}s")
                    continue

                filename = f"frame_{second}_{i}.jpg"
                filepath = os.path.join(output_folder, filename)
                cv2.imwrite(filepath, frame)
                print(f"✅ Saved {filename}")

                # Generate caption from the saved image
                caption = self.describer.description(filepath)
                self.captions_list.append(caption)

                # Delete the image after analysis
                os.remove(filepath)
                print(f"✅ Deleted {filename}")

            second += 1
            current_time = second

        cap.release()
        print("\n✅ All frames extracted, analyzed, and deleted.\nCaptions has been extracted\n")
        return self.captions_list


'''# For testing this module independently:
if __name__ == "__main__":
    obj = GetCaptions()
    captions = obj.extract_images_from_video_returns_list_of_captions(
        video_path="videos/videoplayback.mp4", 
        output_folder="out", 
        fps_extract=2
    )
    print("Extracted Captions:", captions)
'''