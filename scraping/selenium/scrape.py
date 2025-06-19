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
import pandas as pd


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

    if year_index != -1:
        make = parts[0]
        model = " ".join(parts[1:year_index])
        variant = " ".join(parts[year_index + 1:]) if year_index + 1 < len(parts) else ""
        return {
            "Make": make,
            "Model": model,
            "Year": year,
            "Variant": variant
        }
    else:
        return {
            "Make": parts[0] if parts else "Unknown",
            "Model": " ".join(parts[1:]) if len(parts) > 1 else "",
            "Year": "Unknown",
            "Variant": ""
        }
        
def parse_price(text):
    try:
        parts = text.replace(",", "").split()
        amount = float(parts[1])
        unit = parts[2].lower()

        if "lac" in unit:
            return int(amount * 100000)
        elif "crore" in unit:
            return int(amount * 100000000)
        else:
            return int(amount)
    except:
        return "Call"
      
def parse_mileage(text):
    parts = text.replace(",", "").split()
    return int(parts[0])
        
def main():
          
    options = Options()
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")  # recommended for headless
    options.add_argument("--window-size=1920,1080")  # Makes sure elements aren't missing due to viewport


    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service, options=options)

    listings = []

    # Get listings for first 5 pages
    for page in range(1,11):
        url = f'https://www.pakwheels.com/used-cars/search/-/?page={page}'
        driver.get(url)


        try:
          WebDriverWait(driver, 15).until(
              EC.presence_of_element_located((By.CLASS_NAME, "classified-listing"))
          )
        except:
            print(f"Timeout loading page {page}")
            continue

        cars = driver.find_elements(By.CLASS_NAME, "classified-listing")
        for car in cars:
            try:
                # Get car name
                title_element = car.find_element(By.CLASS_NAME, "car-name")
                car_name = title_element.text.strip()
                parsed = parse_listing_name(car_name)

                # Get price
                try:
                    price_text = car.find_element(By.CLASS_NAME, "price-details").text.strip()
                    price = parse_price(price_text)
                    # price = car.find_element(By.CLASS_NAME, "price-details").text.strip()
                    # if "lacs" in price:
                    #   price = int(price[1]*100000)
                    # else:
                    #   price = int(price[1]*10000000)
                except:
                    price = "Call"

                # Get location
                try:
                    location_ul = car.find_element(By.CLASS_NAME, "search-vehicle-info")
                    location = location_ul.find_element(By.TAG_NAME, "li").text.strip()
                except:
                    location = "Unknown"

                # Get mileage
                try:
                    mileage_ul = car.find_element(By.CLASS_NAME, "search-vehicle-info-2")
                    
                    mileage_items = mileage_ul.find_elements(By.TAG_NAME, "li")

                    for li in mileage_items:
                        if "km" in li.text.lower():
                            mileage = parse_mileage(li.text)
                            break
                    
                #   for li in mileage_items:
                #       if "km" in li.text:
                #           mileage = li.text.strip()
                #           break
                except:
                    mileage = "Unknown"

                # Combine all data
                car_data = {
                    **parsed,
                    "Price": price,
                    "Location": location,
                    "Mileage": mileage
                }

                listings.append(car_data)

            except Exception as e:
                print("Error parsing listing:", e)
      
        print(f"✅ Finished page {page}")
        
    driver.quit()

    
    df = pd.DataFrame(listings)
    df.to_csv('cars_data.csv', index=False)

    print("Saved car data to CSV file successfully.")

  
if __name__ == '__main__':
    main()