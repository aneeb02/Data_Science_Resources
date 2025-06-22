from playwright.sync_api import sync_playwright, Playwright
import time


def run(playwright: Playwright):
  start_url = "https://pages.daraz.pk/wow/gcp/route/daraz/pk/upr/router?hybrid=1&data_prefetch=true&prefetch_replace=1&at_iframe=1&wh_pid=%2Flazada%2Fchannel%2Fpk%2Fdaraz-mall%2F%2Fsamsung&spm=a2a0e.tm80335142.bannerSliderDesktop.d_1"
  chrome = playwright.chromium
  browser = chrome.launch(headless=False)
  page = browser.new_page()
  page.goto(start_url)
  
  page.wait_for_selector(".jfy-product-card-component-pc")

  all_products = set()
  prev_height = 0
  scroll_count = 0
  
  while scroll_count < 5:
    products = page.query_selector_all(".jfy-product-card-component-pc")
    for product in products:
      text = product.text_content().strip()
      all_products.add(text)
      #print(product.text_content())
    
    # Scroll to bottom
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    time.sleep(4)  # wait for lazy loading
    new_height = page.evaluate("document.body.scrollHeight")
    time.sleep(2)
    if new_height == prev_height:
        print("No more new products loaded.")
        break
    prev_height = new_height
    scroll_count += 1
      
  for item in all_products:
      print(item[:200])
  
  

with sync_playwright() as p:
  run(p) 