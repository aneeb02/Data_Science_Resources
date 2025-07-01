from playwright.sync_api import sync_playwright, Playwright
import time
import csv
from urllib.request import urlretrieve
import os




def run(playwright: Playwright, query):
  url = 'https://arxiv.org/search/'
  chrome = playwright.chromium
  browser = chrome.launch(headless=False)
  page = browser.new_page()
  page.goto(url)
  
  os.makedirs("data", exist_ok=True)
  
  
  #query = "Deep learning" # change as per requirement
  
  page.get_by_placeholder("Search term...").fill(query)
  page.get_by_role("button", name="Search").nth(1).click()
  
  #time.sleep(2)  --- sleep is built in for playwright
  

  links = page.locator("//a[contains(@href, 'arxiv.org/pdf/')]").all()
  results = page.locator("//li[@class='arxiv-result']")
  
  papers = []
  
  for i in range(results.count()):
    # get title of paper
    title = results.nth(i).locator("p.title").text_content().strip()
    
    # get authors of paper
    authors = results.nth(i).locator("p.authors a").all()
    author_names = [a.text_content().strip() for a in authors]
    author_names = ", ".join(author_names)
        
    # get link to download
    pdf_link = results.nth(i).locator("a[href*='arxiv.org/pdf/']").get_attribute("href")
    
    file_name = pdf_link.split("/")[-1]  # e.g., 2506.22931
    save_path = f"data/{file_name}.pdf"
    
    urlretrieve(pdf_link, save_path)
    print(title, author_names, pdf_link)
    
    papers.append({
      "Title": title,
      "Authors": author_names,
      "PDF Link": pdf_link,
      "Filename": file_name
    })
  
  
  with open("arxiv_papers.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=["Title", "Authors", "PDF Link", "Filename"])
    writer.writeheader()
    writer.writerows(papers)
    
  
  
  # for link in links:
  #   page.goto(link.get_attribute("href"))
  #   page.wait_for_timeout(1000)
  #   page.pdf(path="filename.pdf")  # Works on some sites
  #   print(link.get_attribute("href"))
  
  
with sync_playwright() as p:
  run(p, "deep learning")