from selenium import webdriver  
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import pandas as pd

def toIntPrice(price):
    intPrice = 0
    for l in price:
        if l.isdigit():
            intPrice = intPrice*10 + int(l)
        elif l == '.':
            return intPrice
    return intPrice

def setup_driver():
    chrome_options = Options()
    service = Service()
    return webdriver.Chrome(service=service, options=chrome_options)

def interact_with_form():
    driver = setup_driver()

    try:
        driver.get("https://store.steampowered.com/")
        sec = 1
        time.sleep(3)
        
        wait = WebDriverWait(driver, 10)
        
        topSellersContect = driver.find_element(By.ID, "tab_topsellers_content_trigger")
        driver.execute_script("arguments[0].scrollIntoView(true);", topSellersContect)
        topSellersContect.click()
        
        topSellers = driver.find_element(By.ID, "tab_topsellers_content")
        driver.execute_script("arguments[0].scrollIntoView(true);", topSellers)
        checkBox = topSellers.find_element(By.ID, "topsellers_controls")
        # checkBox.click()
        time.sleep(sec)

        items = topSellers.find_element(By.CLASS_NAME, "tab_content_items")
        games = items.find_elements(By.CLASS_NAME, "tab_item")
        data = []
        
        for game in games:
            time.sleep(sec)

            try:
                name = game.find_element(By.CLASS_NAME, "tab_item_name").text
                author = ''
                release_date = ''
                genre = game.find_element(By.CLASS_NAME, "top_tag").text
                price = game.find_element(By.CLASS_NAME, "discount_final_price").text
                img_url = game.find_element(By.CLASS_NAME, "tab_item_cap_img").get_attribute("src")
                
                if price != 'Free':
                    new_game = [name, author, release_date, genre, toIntPrice(price), img_url]
                    data.append(new_game)

            except Exception as e:
                print(f"Error scraping game")

        df = pd.DataFrame(data, columns=['Name', 'Author', 'Release Date', 'Genre', 'Price', 'img_url'])
        df.to_excel("games.xlsx", index=False, engine="openpyxl")

    except Exception as e:
        print(f"An error occurred: {str(e)}")

    finally:
        time.sleep(sec)
        driver.quit()

# Script entry point
# Only run if this file is run directly (not imported)
if __name__ == "__main__":
    interact_with_form()  # Start the form interaction process