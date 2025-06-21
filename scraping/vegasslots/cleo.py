from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager




def scrape_game_details(driver, url):
    """
    Navigates to a game page and scrapes details using the original user-provided logic.
    This function is designed to be called from scrape.py.
    """
    driver.get(url)

    WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, ".container.mx-auto"))
    )

    # The following logic is preserved exactly from your cleo.py script.
    info_block = driver.find_element(By.CSS_SELECTOR, ".content-visibility.mx-auto.scroll-m-8.bg-white.pb-8.pt-8.md\\:pb-12.md\\:pt-12.lg\\:pb-16.lg\\:pt-16.xl\\:scroll-m-24")

    game_data = {}
    features_checklist = {} # This was in your original code, so it is preserved.

    # left block
    left_block = driver.find_element(By.CSS_SELECTOR, "div.flex-col.gap-4.text-sm")
    lines = left_block.text.split('\n')

    game_data[lines[0]] = lines[1]  # Return to Player
    game_data[lines[2]] = lines[3]  # Volatility
    game_data[lines[4]] = lines[5]  # Provider

    center_block = driver.find_element(By.CSS_SELECTOR, ".flex.h-full.w-full.flex-col.items-start.justify-center.gap-3")
    all_rows = center_block.find_elements(By.CSS_SELECTOR, "div > div")

    # Get the two child columns (left and right halves)
    columns = center_block.find_elements(By.CSS_SELECTOR, "div.w-1\\/2.flex-col.gap-3")

    for col in columns:
        rows = col.find_elements(By.CSS_SELECTOR, "div.flex.flex-row.items-center.justify-between")  # each feature row
        for row in rows:
            try:
                divs = row.find_elements(By.TAG_NAME, 'div')
                if len(divs) < 2:
                    continue

                label = divs[0].text.strip()
                value_div = divs[1]
                value_text = value_div.text.strip()

                if not label:
                    continue

                # Fix Excel layout issue
                if label == "Layout":
                    value_text = "'" + value_text
                try:
                    icon = row.find_element(By.TAG_NAME, 'svg')
                    g_tag = icon.find_element(By.TAG_NAME, 'g')
                    icon_id = g_tag.get_attribute('id')

                    if icon_id == "check-square":
                        game_data[label] = True
                    elif icon_id == "x-square":
                        game_data[label] = False
                    else:
                        game_data[label] = "Unknown"
                except:
                    game_data[label] = "Missing Icon"

            except Exception as e:
                print(f"Failed to extract feature: {e}")

    for row in all_rows:
        parts = row.text.split('\n')
        if len(parts) == 2:
            key = parts[0].strip()
            value = parts[1].strip()
            game_data[key] = value

    return game_data


options = Options()
options.add_argument('--headless')
options.add_argument("--disable-gpu")  # recommended for headless
options.add_argument("--window-size=1920,1080")  # Makes sure elements aren't missing due to viewport

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

# print(scrape_game_details(driver, 'https://www.vegasslotsonline.com/igt/cleopatra/'))
# print(scrape_game_details(driver, 'https://www.vegasslotsonline.com/igt/white-orchid/'))

