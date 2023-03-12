import subprocess

def update_pip():
    subprocess.check_call(['pip','install','--upgrade','pip'])

def install(package):
    subprocess.check_call(['pip', 'install', package])

update_pip()

# Replace 'requests' with any other package you want to install
install('requests')
install("pandas")
install("rasterio")