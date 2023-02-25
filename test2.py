import os
import subprocess

folder_name = "FeatheredMaps"
folder_path = None

# iterate through all the drives on the computer
for drive in ['C:\\', 'D:\\', 'E:\\']:
    # search for the folder in the drive
    for root, dirs, files in os.walk(drive):
        if folder_name in dirs:
            folder_path = os.path.join(root, folder_name)
            break
    # stop searching if the folder is found
    if folder_path:
        break

if folder_path:
    print(f"Folder '{folder_name}' found at '{folder_path}'")
else:
    print(f"Folder '{folder_name}' not found")



# get the Edge browser version using the command line
try:
    command_output = subprocess.check_output("wmic datafile where name=\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\" get Version /value", shell=True, text=True)
    browser_version = command_output.split("=")[1].strip()
    print(f"Edge browser version: {browser_version}")
except subprocess.CalledProcessError:
    print("Microsoft Edge browser is not installed.")
    exit()


# create a new instance of the Edge driver
#driver = webdriver.Edge(executable_path=driver_path)

# navigate to the Microsoft Edge WebDriver download page
#driver.get('https://developer.microsoft.com/en-us/microsoft-edge/tools/webdriver/')