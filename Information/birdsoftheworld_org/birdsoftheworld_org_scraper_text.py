import os

webdriver_folder_name = "Selenium"

# search for .zip file in the folder
for root, dirs, files in os.walk(".", topdown=False):
    for name in files:
        if name.endswith(".exe") and webdriver_folder_name in root:
            zip_file_path = os.path.join(root, name)
            print("Found file:", zip_file_path)

from msedge.selenium_tools import Edge, EdgeOptions

# Create EdgeOptions object and set options
options = EdgeOptions()
options.use_chromium = True

# Create Edge webdriver with options and go to URL
driver = Edge(options=options)
url = r'https://secure.birds.cornell.edu/cassso/login?service=https%3A%2F%2Fbirdsoftheworld.org%2Flogin%2Fcas'
driver.get(url)


# Keep the browser window open
input("Press Enter to close the browser")
driver.quit()
