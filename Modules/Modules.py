import subprocess

def update_pip():
    subprocess.check_call(['pip','install','--upgrade','pip'])

def install(Packages):
    for package in Packages:
        subprocess.check_call(['pip', 'install', package ])

update_pip()

# Replace 'requests' with any other package you want to install
Packages = [
"requests",
"pandas",
#"rasterio",
#"matplotlib",
"ipyleaflet"
"tqdm"
]

install(Packages)