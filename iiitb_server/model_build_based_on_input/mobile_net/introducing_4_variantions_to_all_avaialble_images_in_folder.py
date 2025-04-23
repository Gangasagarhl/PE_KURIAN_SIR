import cv2
import albumentations as A
import os
import shutil

class image_preperation:
    def __init__(self):
        print("Initiated\n")

    def read_and_resize_the_image(self, img_path):
        # Load image
        img = cv2.imread(img_path)
        if img is None:
            print(f"[ERROR] Failed to read image: {img_path}")
            return None
        # Resize to 224x224
        resized_img = cv2.resize(img, (224, 224))
        return resized_img

    def transformation_on_images(self, img, folder_name, count):
        # Ensure 'modified' directory exists
        modified_dir = os.path.join(folder_name, "modified")
        os.makedirs(modified_dir, exist_ok=True)

        # Define augmentation pipelines with a border_mode to avoid black borders
        augment1 = A.Compose([
            A.Rotate(limit=30, p=0.8, border_mode=cv2.BORDER_REPLICATE)
        ])
        augment2 = A.Compose([
            A.Rotate(limit=30, p=0.8, border_mode=cv2.BORDER_REPLICATE),
            A.HorizontalFlip(p=0.5)
        ])
        augment3 = A.Compose([
            A.Rotate(limit=30, p=0.8, border_mode=cv2.BORDER_REPLICATE),
            A.HorizontalFlip(p=0.5),
            A.RandomBrightnessContrast(p=0.3)
        ])
        augment4 = A.Compose([
            A.Rotate(limit=30, p=0.8, border_mode=cv2.BORDER_REPLICATE),
            A.HorizontalFlip(p=0.5),
            A.RandomBrightnessContrast(p=0.3),
            A.ElasticTransform(p=0.2, border_mode=cv2.BORDER_REPLICATE)
        ])

        # Save original image
        cv2.imwrite(os.path.join(modified_dir, f"original_{count}.jpg"), img)

        # Apply augmentations
        for idx, aug in enumerate([augment1, augment2, augment3, augment4], start=1):
            augmented = aug(image=img)["image"]
            output_path = os.path.join(modified_dir, f"{count}_{idx}.jpg")
            cv2.imwrite(output_path, augmented)

    def list_all_images_in_folder(self, folder_path):
        return os.listdir(folder_path)

    def delete_files_from_list(self, folder_path, file_list):
        for filename in file_list:
            file_path = os.path.join(folder_path, filename)
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {filename}")
            else:
                print(f"File not found: {filename}")

    def rename_folders(self, folder_path, old_name, new_name):
        old_folder = os.path.join(folder_path, old_name)
        new_folder = os.path.join(folder_path, new_name)

        if os.path.exists(old_folder):
            os.rename(old_folder, new_folder)
            print(f"Renamed: {old_name} → {new_name}")
        else:
            print(f"Folder not found: {old_name}")

    def move_folder(self, source_folder, destination_folder):
        os.makedirs(destination_folder, exist_ok=True)
        try:
            shutil.move(source_folder, destination_folder)
            print(f"Moved folder: {source_folder} → {destination_folder}")
        except Exception as e:
            print(f"Error moving folder: {e}")

    def apply_transformation_for_every_image(self, folder_path, name):
        li = self.list_all_images_in_folder(folder_path=folder_path)
        count = 0

        for i in li:
            full_path = os.path.join(folder_path, i)
            print(f"Processing: {full_path}")

            # Skip non-image files
            if not (i.lower().endswith(".jpg") or i.lower().endswith(".jpeg") or i.lower().endswith(".png")):
                print(f"Skipped (not an image): {i}")
                continue

            image = self.read_and_resize_the_image(full_path)
            if image is None:
                print(f"Skipped (could not read image): {i}")
                continue

            self.transformation_on_images(image, folder_name=folder_path, count=count)
            count += 30000

        # Delete original images
        self.delete_files_from_list(folder_path=folder_path, file_list=li)

        # Rename the folder
        self.rename_folders(folder_path=folder_path, old_name="modified", new_name=name)

        # Move to destination folder
        self.move_folder(source_folder=os.path.join(folder_path, name), destination_folder='database')

if __name__ == "__main__":
    image = image_preperation()
    image.apply_transformation_for_every_image("downloaded_images/", 'BOTTLE')

