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
        sec = 1
        time.sleep(5)
        
        wait = WebDriverWait(driver, 10)
        
        
        topSellersContect = driver.find_element(By.ID, "tab_topsellers_content_trigger")
        driver.execute_script("arguments[0].scrollIntoView(true);", topSellersContect)
        topSellersContect.click()
        
        topSellers = driver.find_element(By.ID, "tab_topsellers_content")
        driver.execute_script("arguments[0].scrollIntoView(true);", topSellers)
        time.sleep(sec)

        items = topSellers.find_element(By.CLASS_NAME, "tab_content_items")
        games = items.find_elements(By.CLASS_NAME, "tab_item")
        data = []
        
        for game in games:
            time.sleep(sec)
            game_link = game.get_attribute("href")
            if not game_link:
                continue
            driver.get(game_link)
            time.sleep(1)

            try:
                name = driver.find_element(By.CLASS_NAME, "appHubAppName").text
                author = driver.find_element(By.ID, "developers_list").text 
                release_date = driver.find_element(By.CLASS_NAME, "date").text
                genres_list = []
                genres_tags = driver.find_element(By.CLASS_NAME, "glance_tags popular_tags")
                genres = genres_tags.find_elements(By.CLASS_NAME, "app_tag")
                for i in range(2):
                    genres_list.append(genres[i].text)
                price = driver.find_element(By.CLASS_NAME, "game_purchase_price price").text
                img_url = driver.find_element(By.CLASS_NAME, "game_header_image_full").get_attribute("src")
                
                new_game = [name, author, release_date, genres_list, price, img_url]
                print(new_game)
                data.append(new_game)

            except Exception as e:
                print(f"Error scraping game")
                
            time.sleep(1)
            driver.back()
            time.sleep(1)
            

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
    print("Not working :P")
    # interact_with_form()  # Start the form interaction process