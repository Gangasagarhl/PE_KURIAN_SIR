from transformers import BlipProcessor, BlipForConditionalGeneration
import warnings
import torch
import cv2
import os
from PIL import Image  # Import PIL for image loading

warnings.filterwarnings("ignore")

class image_description:
    def __init__(self,blip_model,blip_processor):
        # Use local folder where the BLIP model is saved.
        self.processor = blip_processor
        self.model =blip_model


        print("\n\n*********BLIP MODEL DOWNLOADED*********\n\n")

    def description(self, image_path):
        # Load the image from the provided file path
        image = Image.open(image_path).convert("RGB")
        inputs = self.processor(images=image, return_tensors="pt")
        
        # Generate caption
        output = self.model.generate(**inputs)
        caption = self.processor.decode(output[0], skip_special_tokens=True)
        return caption

class get_captions:
    def __init__(self,blip_model,blip_processor):
        self.describer = image_description(blip_model,blip_processor)
        self.captions_list = []

    def extract_images_from_video_returns_list_of_captions(self, video_path, output_folder, fps_extract=1):
        if not os.path.exists(output_folder):
            os.makedirs(output_folder)

        cap = cv2.VideoCapture(video_path)
        video_fps = cap.get(cv2.CAP_PROP_FPS)
        total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / video_fps

        print(f"🎥 Video loaded. Duration: {duration:.2f}s, FPS: {video_fps}")

        current_time = 0.0
        second = 0

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

                # Call the description function on the saved image path
                caption = self.describer.description(filepath)
                self.captions_list.append(caption)

                # Delete the image after analysis
                os.remove(filepath)
                print(f"✅ Deleted {filename}")

            second += 1
            current_time = second

        cap.release()
        print("\n✅ All frames extracted, analyzed, and deleted.")
        return self.captions_list

if __name__ == "__main__":
    obj = get_captions()
    captions = obj.extract_images_from_video_returns_list_of_captions(
        video_path="videos/videoplayback.mp4", 
        output_folder="out", 
        fps_extract=2
    )
    print(captions)
