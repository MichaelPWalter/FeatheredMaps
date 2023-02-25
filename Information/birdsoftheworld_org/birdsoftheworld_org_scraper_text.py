from selenium import webdriver
import pandas as pd
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException
import re



def login(driver):

    # Define your credentials
    username= input("eBird Username: ")
    password= input("eBird Password")

    # Navigate to the login page
    driver.get("https://secure.birds.cornell.edu/cassso/login?service=https%3A%2F%2Fbirdsoftheworld.org%2Flogin%2Fcas")

    # Find the username and password fields and enter your credentials
    username_field = driver.find_element(By.ID, "input-user-name")
    username_field.clear()
    username_field.send_keys(username)

    password_field = driver.find_element(By.ID, "input-password")
    password_field.clear()
    password_field.send_keys(password)

    # Click the login button
    login_button = driver.find_element(By.ID, "form-submit")
    login_button.click()

    # Wait for the page to load after login
    wait = WebDriverWait(driver, 10)


# Define clean_text function
def clean_text(text):
    # Remove '\nphoto\n' and '\nvideo\n'
    text = text.replace('\nphoto\n', '')
    text = text.replace('\nvideo\n', '')
    
    # Remove all parentheses containing numbers
    text = re.sub(r'\([^()]*\d+[^()]*\)', '', text)
    
    # Remove extra whitespace
    text = re.sub('\s+', ' ', text).strip()

    return text

# Set up the webdriver
driver = webdriver.Edge(executable_path="./Selenium/edgedriver_win64/msedgedriver.exe")

# login to birdsoftheworld.org
login(driver)

# Load CSV
df = pd.read_csv('Information/birdsoftheworld_org/ebird_taxonomy_v2022_standardized.csv')

# Scrape website for each row
for i, row in df.iterrows():
    # Get the eBird_Species_Code value for the current row
    species_code = row['eBird_Species_Code']
    
    # Construct the URL for the species page
    driver.get(f"https://birdsoftheworld.org/bow/species/{species_code}/cur/introduction")

    # Wait for page to load
    driver.implicitly_wait(10)

    # Find all paragraphs with class 'u-stack-lg u-text-4-loose u-article'
    paragraphs = driver.find_elements(By.CLASS_NAME, 'u-stack-lg.u-text-4-loose.u-article')

    # Iterate over paragraphs
    for paragraph in paragraphs:
        # Get section name from aria-labelledby
        try:
            section_name = paragraph.get_attribute('aria-labelledby')
        except NoSuchElementException:
            section_name = 'Unknown'

        # Add section name as column if it doesn't exist
        if section_name not in df.columns:
            df[section_name] = ''

        paragraph_text = clean_text(paragraph.text)

        # Append text to section column
        df.at[i, section_name] += ' ' + paragraph_text

# Save updated CSV
df.to_csv('updated_file.csv', index=False)

# Quit driver
driver.quit()