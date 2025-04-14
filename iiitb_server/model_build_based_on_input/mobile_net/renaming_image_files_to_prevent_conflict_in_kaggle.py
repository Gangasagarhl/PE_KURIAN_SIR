import os

def change_the_name_of_file(folder_path):
    count = 0
    for i in sorted(os.listdir(folder_path)):
        src = os.path.join(folder_path, i)

        # Skip if not a file or not an image
        if not os.path.isfile(src) or not i.lower().endswith(('.jpg', '.jpeg', '.png')):
            continue

        # Get original extension
        ext = os.path.splitext(i)[1].lower()
        dst = os.path.join(folder_path, str(folder_path[-1])+f"{count}{ext}")

        os.rename(src, dst)
        print(f"Renamed: {i} → {count}{ext}")
        count += 1

        
if __name__ == "__main__": 
    change_the_name_of_file("database/BOTTLE")
    change_the_name_of_file("database/NO")

