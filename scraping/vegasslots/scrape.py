import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from cleo import scrape_game_details

import time
import pandas as pd


data = {}
slots = []

options = Options()
options.add_argument('--headless')
options.add_argument("--disable-gpu")  # recommended for headless
options.add_argument("--window-size=1920,1080")  # Makes sure elements aren't missing due to viewport

service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)

url = "https://www.vegasslotsonline.com/free/"
driver.get(url)

WebDriverWait(driver, 15).until(
              EC.presence_of_element_located((By.CLASS_NAME, "grid-cols-2"))
)

titles = driver.find_elements(By.CSS_SELECTOR, '[data-testid="card-slot"]')

for title in titles:
  lines = title.text.split('\n') 
  name = lines[0]
  dev = lines[1] if len(lines) > 1 else 'Not Listed'
  img = title.find_element(By.TAG_NAME, 'img')
  img_url = img.get_attribute('src')
  play = title.find_element(By.TAG_NAME, 'a')
  play_link = play.get_attribute('href')  
  
  data = {
    "Name": name,
    "Developer": dev,
    "Image URL": img_url,
    "Link": play_link
  }
  slots.append(data)
  


for slot in slots[:20]:
  url = slot["Link"]
  print(f'Parsing: {url}')
  
  try:
      details = scrape_game_details(driver, url)
      slot.update(details)
  except Exception as e:
      print(f"❌ Failed to scrape {url}: {e}")
  time.sleep(1.2)

df = pd.DataFrame(slots)
df.to_csv("all_games_data.csv", index=False)

driver.quit()