from fuzzywuzzy import fuzz

s1 = "neotropical comorant"
s2 = "neotropic cormorant"
threshold = 90  # set the threshold for a match

score = fuzz.token_set_ratio(s1, s2)
if score >= threshold:
    print(f"Strings match with score {score}")
else:
    print("Strings do not match")


import subprocess

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
