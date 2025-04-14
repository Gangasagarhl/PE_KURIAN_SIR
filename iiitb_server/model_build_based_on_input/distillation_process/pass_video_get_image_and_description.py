import cv2
import sys
from pathlib import Path

# Add grandparent directory to Python path for importing modules



def extract_images_from_videos(input_folder, output_folder, images_per_second=2):
    input_folder = Path(input_folder)
    output_folder = Path(output_folder)
    output_folder.mkdir(parents=True, exist_ok=True)
    
    # Supported video extensions
    video_extensions = {".mp4", ".webm", ".avi", ".mov", ".mkv", ".flv", ".mpeg", ".mpg", ".wmv"}

    for video_file in input_folder.glob("*"):
        if video_file.suffix.lower() not in video_extensions:
            continue  # Skip non-video files

        video_name = video_file.stem
        video_output_dir = output_folder / video_name
        #video_output_dir.mkdir(parents=True, exist_ok=True)

        cap = cv2.VideoCapture(str(video_file))
        if not cap.isOpened():
            print(f"[ERROR] Failed to open video: {video_file}")
            continue

        fps = cap.get(cv2.CAP_PROP_FPS)
        frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        duration = int(frame_count / fps)

        saved_count = 0

        for sec in range(duration):
            # Get time offsets per second
            offsets = (
                [0.5] if images_per_second == 1
                else [i / images_per_second for i in range(images_per_second)]
            )

            for offset in offsets:
                msec = (sec + offset) * 1000
                cap.set(cv2.CAP_PROP_POS_MSEC, msec)
                ret, frame = cap.read()
                if not ret:
                    continue

                img_filename = f"out/{video_name}_frame{saved_count:05d}.jpg"
                cv2.imwrite(str(img_filename), frame,[cv2.IMWRITE_JPEG_QUALITY, 70])

                #caption = description(frame)
                #insert_sentences_into_csv(str(img_filename), caption,"data.csv")

                saved_count += 1

        cap.release()
        print(f"[INFO] Processed {video_file.name}: saved {saved_count} images")

    print("[DONE] All videos processed.")

if __name__ == "__main__":
    input_videos_folder = "videos/"
    output_images_folder = "out/"
    extract_images_from_videos(input_videos_folder, output_images_folder, images_per_second=2)
