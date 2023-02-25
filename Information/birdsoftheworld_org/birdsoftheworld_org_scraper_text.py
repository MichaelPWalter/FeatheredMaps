import subprocess
import webbrowser

# get the Edge browser version using the command line
try:
    command_output = subprocess.check_output("wmic datafile where name=\"C:\\\\Program Files (x86)\\\\Microsoft\\\\Edge\\\\Application\\\\msedge.exe\" get Version /value", shell=True, text=True)
    browser_version = command_output.split("=")[1].strip()
    print(f"Edge browser version: {browser_version}")
except subprocess.CalledProcessError:
    print("Microsoft Edge browser is not installed.")
    exit()


url = f'https://msedgedriver.azureedge.net/{browser_version}/edgedriver_win64.zip'
webbrowser.open_new_tab(url)