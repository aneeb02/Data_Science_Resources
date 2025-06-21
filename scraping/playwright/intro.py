from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup as bs
import json

with sync_playwright() as p:
  browser = p.chromium.launch(headless=False, slow_mo=50)
  page = browser.new_page()
  page.goto("https://quotes.toscrape.com/")
  
  page_num = 1
  all_quotes = []

  #total 10 pages
  while page_num <=10:
    print(f"Scraping Page: {page_num}")

    html = page.inner_html("div.container")
    soup = bs(html, 'html.parser')
    quotes = soup.find_all('div', {"class": "quote"})
    
    for quote in quotes:
      q = quote.find('span', {"class": "text"}).text.strip()
      author = quote.find('small', {"class": "author"}).text.strip()
      tags = quote.find_all('a', {"class": "tag"})
      tags_list = []
      for tag in tags:
        tags_list.append(tag.text.strip())
      
      all_quotes.append({
          "Quote": q,
          "Author": author,
          "Tags": tags_list
      })
      
    next_button = page.query_selector("li.next a")
    if next_button:
        print("Navigating to the next page...")
        next_button.click()
        # Wait for the next page to fully load
        page.wait_for_load_state("load") 
        page_num += 1
    else:
        # If no "Next" button is found, stop the loop
        print("No more pages found.")
        break
          
  browser.close()

#save data to json
with open("quotes.json", "w", encoding="utf-8") as f:
    json.dump(all_quotes, f, ensure_ascii=False, indent=2)

print(f"\nSuccessfully saved {len(all_quotes)} quotes to quotes.json")


  #Alternate method
  # Select all quote elements
  # quote_elements = page.query_selector_all("div.quote")

  # for quote in quote_elements:
  #     text = quote.query_selector("span.text").inner_text()
  #     author = quote.query_selector("small.author").inner_text()
  #     tags = [tag.inner_text() for tag in quote.query_selector_all("div.tags a.tag")]
  #     print({
  #         "text": text,
  #         "author": author,
  #         "tags": tags
  #     })
