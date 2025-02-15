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
        driver.get("https://store.steampowered.com/")
        time.sleep(5)

        wait = WebDriverWait(driver, 10)
        
        topSellers = driver.find_element(By.CLASS_NAME, "tab_content")
        driver.execute_script("arguments[0].scrollIntoView(true);", topSellers)
        
        data = []
        game_links = topSellers.find_elements(By.TAG_NAME, "a")
        
        for i, game in enumerate(game_links[:3]):  # חפש 3 משחקים בלבד
            game_link = game.get_attribute("href")

            if not game_link:
                continue

            driver.get(game_link)  # עבור לדף המשחק
            time.sleep(2)

            try:
                name = driver.find_element(By.ID, "appHubAppName").text
                author = driver.find_element(By.ID, "developers_list").text
                release_date = driver.find_element(By.CLASS_NAME, "date").text
                genre = driver.find_element(By.CLASS_NAME, "app_tag").text
                price = driver.find_element(By.CLASS_NAME, "game_purchase_price").text
                img_url = driver.find_element(By.CLASS_NAME, "game_header_image_full").get_attribute("src")

                data.append([name, author, release_date, genre, price, img_url])

            except Exception as e:
                print(f"Error scraping game {i+1}: {str(e)}")

            driver.back()
            time.sleep(2)

        df = pd.DataFrame(data, columns=['Name', 'Author', 'Release Date', 'Genre', 'Price', 'img_url'])
        df.to_excel("games.xlsx", index=False, engine="openpyxl")
            
        for i in data:
            print(i)

    except Exception as e:
        print(f"An error occurred: {str(e)}")  # Print any errors that occur

    finally:
        driver.quit()  # Close the browser, regardless of success or failure

# Script entry point
# Only run if this file is run directly (not imported)
if __name__ == "__main__":
    interact_with_form()  # Start the form interaction process