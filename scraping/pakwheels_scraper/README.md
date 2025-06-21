# PakWheels Scraper

This project scrapes car data from PakWheels.com, a popular automotive portal in Pakistan.

## Functionality

The main script, `scrape.py`, uses Selenium and BeautifulSoup to navigate through the used car listings on PakWheels.com. It extracts details for each car, including:

- Make
- Model
- Year
- Variant
- Mileage
- Price
- Location

The script is designed to scrape data from the first 10 pages of the search results.

The `pw.py` script appears to be an earlier or experimental version for scraping data and might not be the primary script to use.

## How to Run

1.  **Install dependencies:**
    Ensure you have Python installed. You'll also need to install the required libraries:
    ```bash
    pip install requests beautifulsoup4 selenium webdriver-manager pandas
    ```
    This project uses `webdriver-manager` to automatically download and manage the appropriate ChromeDriver.

2.  **Run the scraper:**
    Navigate to the `scraping/pakwheels_scraper` directory and execute the `scrape.py` script:
    ```bash
    python scrape.py
    ```

## Output

The scraped data is saved in a CSV file named `cars_data.csv` in the `scraping/pakwheels_scraper` directory. Each row in the CSV represents a car listing with its extracted details.

**Note:** Web scraping can be affected by changes in the website's structure. If the scraper stops working, it might be necessary to update the selectors and parsing logic in `scrape.py`.
