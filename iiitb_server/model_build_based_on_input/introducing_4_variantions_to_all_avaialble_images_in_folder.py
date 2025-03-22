import cv2
import albumentations as A
import os
import shutil
import os

class image_preperation:
    def __init__(self):
        print("Initiated\n")
    def read_and_resize_the_image(self,img_path):
        # Load image
        img = cv2.imread(img_path)

        # Resize to 256x256
        resized_img = cv2.resize(img, (224, 224))
        return resized_img



    def transformation_on_images(self, img, folder_name, count):
    # Ensure 'modified' directory exists
        modified_dir = os.path.join(folder_name, "modified")
        os.makedirs(modified_dir, exist_ok=True)  # Create if not exists

        # Define an augmentation pipeline
        augment1 = A.Compose([A.Rotate(limit=30, p=0.8)])
        augment2 = A.Compose([A.Rotate(limit=30, p=0.8), A.HorizontalFlip(p=0.5)])
        augment3 = A.Compose([A.Rotate(limit=30, p=0.8), A.HorizontalFlip(p=0.5), A.RandomBrightnessContrast(p=0.3)])
        augment4 = A.Compose([A.Rotate(limit=30, p=0.8), A.HorizontalFlip(p=0.5), A.RandomBrightnessContrast(p=0.3), A.ElasticTransform(p=0.2)])
        
        cv2.imwrite(modified_dir+"/original_"+str(count)+".jpg",img)
        # Apply augmentations
        for idx, aug in enumerate([augment1, augment2, augment3, augment4], start=1):
            augmented = aug(image=img)["image"]
            output_path = os.path.join(modified_dir, f"{count}_{idx}.jpg")
            cv2.imwrite(output_path, augmented)
        
        

        
    def list_all_images_in_folder(self,folder_path):
        lst = os.listdir(folder_path)
        return lst
    
    
        
    
    
    def delete_files_from_list(self,folder_path, file_list):
   
        for filename in file_list:
            file_path = os.path.join(folder_path, filename)
            
            if os.path.exists(file_path):
                os.remove(file_path)
                print(f"Deleted: {filename}")
            else:
                print(f"File not found: {filename}")
                
    
    def rename_folders(self,folder_path, old_name, new_name):
        """
        Renames a folder in the specified directory.

        Args:
        - folder_path (str): Path to the parent folder.
        - old_name (str): Current name of the folder.
        - new_name (str): New name for the folder.
        """
        
        old_folder = os.path.join(folder_path, old_name)
        new_folder = os.path.join(folder_path, new_name)

        if os.path.exists(old_folder):
            os.rename(old_folder, new_folder)
            print(f"Renamed: {old_name} → {new_name}")
        else:
            print(f"Folder not found: {old_name}")
            
            
    def move_folder(self,source_folder, destination_folder):
   
        # Ensure the destination folder exists
        os.makedirs(destination_folder, exist_ok=True)
        
        try:
            # Move the folder
            shutil.move(source_folder, destination_folder)
            print(f"Moved folder: {source_folder} → {destination_folder}")
        
        except Exception as e:
            print(f"Error: {e}")
              
    
    def apply_transformation_for_every_image(self,folder_path,name): 
        li = self.list_all_images_in_folder(folder_path=folder_path)
        
        count= 0
        for i in li:
            print(folder_path+"/"+i)
            image =  self.read_and_resize_the_image(folder_path+"/"+i)
            
            self.transformation_on_images(image,folder_name=folder_path,count=count)
            count+=1
        
        #delete the original images 
        self.delete_files_from_list(folder_path=folder_path, file_list=li)
        
        #rename the folder name
        self.rename_folders(folder_path=folder_path, old_name="modified", new_name=name)
        
        #Now transfer the modified folder 
        self.move_folder(source_folder=folder_path+"/"+name, destination_folder='database')
                
                
        """
        folder_path = "path/to/your/folder" # Folder containing the files
        file_list = ["file1.png", "file2.jpg", "file3.mp4"]  # List of files to delete
        delete_files_from_list(folder_path, file_list)
        """
        
        
    

    
            
if __name__ ==  "__main__":
    
    image  =  image_preperation()
    #image.apply_transformation_for_every_image("downloaded_images", 'NO')
    image.move_folder("downloaded_images/NO", "database")
    


    