from selenium import webdriver  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def setup_driver():
    chrome_options = Options()
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)

def interact_with_form():
    driver = setup_driver()

    try:
        df = pd.read_excel('games.xlsx', engine='openpyxl')
        df = pd.read_excel('games.xlsx', usecols=['Name', 'Genre', 'Price'], engine='openpyxl')
        
        driver.get("https://store.steampowered.com/")
        # time.sleep(2)

        # Create a wait object with 10-second timeout
        wait = WebDriverWait(driver, 10)
        
         # Handle form submission
        addGame_button = driver.find_element(By.ID, "submit")  # Find submit button

        # Handle the name field
        title_field = wait.until(EC.presence_of_element_located((By.ID, "userName")))  # Wait until name field is present
        title_field.send_keys("John")  # Type "John"
        time.sleep(1)  # Wait 1 second

        # Handle the email field
        genre_field = driver.find_element(By.ID, "userEmail")  # Find email input field
        genre_field.send_keys("john")  # Type first part
        time.sleep(1)

        # Handle current address field
        price_field = driver.find_element(By.ID, "currentAddress")  # Find address input
        price_field.send_keys("123 Main Street")  # Type street
        time.sleep(1)

        # Scroll to make button visible
        driver.execute_script("arguments[0].scrollIntoView(true);", addGame_button)
        time.sleep(1)  # Wait after scrolling
        addGame_button.click()  # Click the submit button

        time.sleep(3)  # Wait to see the results

        # Wait for user input before closing
        input("Press Enter to close the browser...")

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Print any errors that occur

    finally:
        driver.quit()  # Close the browser, regardless of success or failure

# Script entry point
# Only run if this file is run directly (not imported)
if __name__ == "__main__":
    interact_with_form()  # Start the form interaction process