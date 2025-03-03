# /opt/anaconda3/bin/python sel.py
# Import statements
from selenium import webdriver  # Main Se

# lenium package for browser automation
# Manages ChromeDriver service
from selenium.webdriver.chrome.service import Service

# Chrome-specific configuration options
from selenium.webdriver.chrome.options import Options

# Provides locator strategies (ID, CLASS, etc.)
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # Implements explicit waits

# Conditions for WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time  # For adding delays between actions
# Function to set up the Chrome WebDriver

import pandas as pd

def setup_driver():
    chrome_options = Options()  # Create a new Options object for Chrome
    service = Service()  # Create a new Service object to manage ChromeDriver
    # Initialize Chrome with our settings
    return webdriver.Chrome(service=service, options=chrome_options)

def interact_with_form():
    driver = setup_driver()  # Create a new browser instance

    try:
        df = pd.read_excel('games.xlsx', engine='openpyxl')
        df = pd.read_excel('games.xlsx', usecols=['Name', 'Genre', 'Price'], engine='openpyxl')
        # Open the website
        # Navigate to the specified URL
        driver.get("http://127.0.0.1:5500/frontend/index.html")
        # time.sleep(2)  # Pause for 2 seconds to let the page load

        # Create a wait object with 10-second timeout
        wait = WebDriverWait(driver, 10)
        
        username_field = driver.find_element(By.ID, "username")
        username_field.send_keys("admin")
        time.sleep(1)
        password_field = driver.find_element(By.ID, "password")
        password_field.send_keys("123")
        time.sleep(1)
        login_button = driver.find_element(By.ID, "login")
        login_button.click()
        time.sleep(1)
        
        driver.switch_to.alert.accept()
        time.sleep(1)
        
        name_field = wait.until(EC.presence_of_element_located((By.ID, "game-name"))) # Handle the game name field
        genre_field = driver.find_element(By.ID, "game-genre") # Handle the game genre field
        price_field = driver.find_element(By.ID, "game-price") # Handle the game price field
        
        # Handle form submission
        addGame_button = driver.find_element(By.ID, "addgame-btn")  # Find submit button
        driver.execute_script("arguments[0].scrollIntoView(true);", addGame_button) # Scroll to make button visible
            
        for index, row in df.iterrows():
            wait.until(EC.presence_of_element_located((By.ID, "game-name"))).send_keys(str(row['Name']))
            time.sleep(1)
            driver.find_element(By.ID, "game-genre").send_keys(str(row['Genre']))
            time.sleep(1)
            driver.find_element(By.ID, "game-price").send_keys(int(row['Price']))
            time.sleep(1)
            addGame_button.click()
            time.sleep(1)
            driver.switch_to.alert.accept()
            time.sleep(1)
        
        time.sleep(3)  # Wait to see the results

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Print any errors that occur
    finally:
        driver.quit()  # Close the browser, regardless of success or failure

# Script entry point
# Only run if this file is run directly (not imported)
if __name__ == "__main__":
    interact_with_form()  # Start the form interaction process