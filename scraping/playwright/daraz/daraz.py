from playwright.sync_api import sync_playwright, Playwright
import time


def run(playwright: Playwright):
  start_url = "https://pages.daraz.pk/wow/gcp/route/daraz/pk/upr/router?hybrid=1&data_prefetch=true&prefetch_replace=1&at_iframe=1&wh_pid=%2Flazada%2Fchannel%2Fpk%2Fflashsale%2F7cdarZ6wBa&hide_h5_title=true&lzd_navbar_hidden=true&spm=a2a0e.tm80335142.bannerSliderDesktop.d_2"
  chrome = playwright.chromium
  browser = chrome.launch(headless=False)
  page = browser.new_page()
  page.goto(start_url)
  
  page.wait_for_selector(".aplus-common-data-tracker.flash-unit-a")

  all_products = []
  prev_height = 0
  scroll_count = 0
  
  for i in range(2):
    products = page.query_selector_all(".aplus-common-data-tracker.flash-unit-a")
    for product in products:
      title = product.query_selector(".sale-title").text_content().strip() 
      price = product.query_selector(".sale-price").text_content().strip() 
      discount = product.query_selector(".discount").text_content()
      raw_link = product.get_attribute("href")
      
      # Build proper product URL
      if raw_link:
          if raw_link.startswith("//"):
              link = "https:" + raw_link
          elif raw_link.startswith("/"):
              link = "https://www.daraz.pk" + raw_link
          elif raw_link.startswith("http"):
              link = raw_link
          else:
              link = None
      else:
          link = None
      
      if link:
        prod_page = browser.new_page()
        prod_page.goto(link)
        time.sleep(2)
        
        # Scroll to bottom
        prod_page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(2)

        # prod_page.wait_for_selector(".score-average", timeout=10000)
        # rating_el = prod_page.query_selector(".score-average")
        try:
            prod_page.wait_for_selector(".score-average", timeout=5000)
            rating = prod_page.query_selector(".score-average").text_content().strip()
        except:
            rating = "No rating"

        try:
            total_ratings = prod_page.query_selector("div.count").text_content().strip()
        except:
            total_ratings = "No count"
        prod_page.close()    

      p = {
        "Product": title,
        "Price": price,
        "Total Discount": discount,
        "Rating": rating,
        "Total Ratings": total_ratings      
      }
      print(p)
      all_products.append(p)
    
    # Try clicking "Load More"
    try:
        load_more = page.query_selector(".flash-sale-load-more.J_LoadMore")
        if load_more and load_more.is_visible():
            print("Clicking Load More button...")
            load_more.scroll_into_view_if_needed()
            time.sleep(1)
            load_more.click()
            page.wait_for_timeout(2000)  # wait for new products
        else:
            print("Load More not found or not visible.")
            break
    except Exception as e:
        print("Error while clicking Load More:", e)
        break
      
  for item in all_products:
      print(item,'\n')

with sync_playwright() as p:
  run(p)