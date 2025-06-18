import requests
from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
import time

def parse_listing_name(name):
    parts = name.split()
    year = None
    year_index = -1
    
    if 'for' in parts:
        for_index = parts.index('for')
        parts = parts[:for_index]

    for i in reversed(range(len(parts))):
        if parts[i].isdigit() and len(parts[i]) == 4 and (parts[i].startswith('20') or parts[i].startswith('19')):
            year = parts[i]
            year_index = i
            break
          
    try:
      mileage_ul = car.find_element(By.CLASS_NAME, "search-vehicle-info-2")
      mileage_items = mileage_ul.find_elements(By.TAG_NAME, "li")
      
      mileage = ""
      for li in mileage_items:
          if "km" in li.text:
              mileage = li.text.strip()
              break
    except:
        mileage = "Unknown"
        
    
    if year_index != -1:
        make = parts[0]
        model = " ".join(parts[1:year_index])
        variant = " ".join(parts[year_index + 1:]) if year_index + 1 < len(parts) else ""
        price = driver.find_element(By.CLASS_NAME, 'price-details').text
        location = driver.find_element(By.CSS_SELECTOR, "ul.search-vehicle-info > li").text
        mileage=mileage
        
        return {
            "Make": make,
            "Model": model,
            "Year": year,
            "Variant": variant,
            "Mileage": mileage,
            "Price": price,
            "Location": location
        }
    else:
        return {
            "Make": parts[0] if parts else "Unknown",
            "Model": " ".join(parts[1:]) if len(parts) > 1 else "",
            "Year": "Unknown",
            "Variant": "",
            "Mileage": mileage,
            "Price": price,
            "Location": location 
        }
        
options = Options()
options.add_argument('--headless')
options.add_argument("--disable-gpu")  # recommended for headless
options.add_argument("--window-size=1920,1080")  # Makes sure elements aren't missing due to viewport


service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(service=service, options=options)


driver.get("https://www.pakwheels.com/used-cars/search/-/")


listings = []

WebDriverWait(driver, 15).until(
    EC.presence_of_element_located((By.CLASS_NAME, "classified-listing"))
)

cars = driver.find_elements(By.CLASS_NAME, "classified-listing")

for car in cars:
  if car.text.split('\n')[1] == "FEATURED":
    car_name = car.text.split('\n')[3]
    parsed = parse_listing_name(car_name)
    listings.append(parsed)
    
  else:
    car_name = car.text.split('\n')[2]
    parsed = parse_listing_name(car_name)
    listings.append(parsed)
    
for l in listings:
  print(l,sep='\n')

driver.quit()