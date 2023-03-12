import os
import zipfile

folder_name = "Selenium"

# search for .zip file in the folder
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name.endswith(".exe") and folder_name in root:
            zip_file_path = os.path.join(root, name)
            print("Found file:", zip_file_path)
            
            # unzip the file in the same directory
            with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
                zip_ref.extractall(os.path.join(root, os.path.splitext(name)[0]))