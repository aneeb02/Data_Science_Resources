# VegasSlotsOnline Scraper

This project scrapes information about online slot games from vegasslotsonline.com.

## Functionality

The project consists of two main Python scripts:

1.  **`scrape.py`**: This is the main script that drives the scraping process.
    *   It first fetches a list of slot games from the free games page (`https://www.vegasslotsonline.com/free/`).
    *   For each game, it extracts basic information like the game's name, developer, a URL to an image of the game, and a direct link to play the game.
    *   It then iterates through a subset of these games (currently the first 20) and navigates to each game's individual page using the `Link`.
    *   On each game page, it calls the `scrape_game_details` function from `cleo.py` to extract more detailed information.
    *   All collected data is then compiled and saved.

2.  **`cleo.py`**: This script acts as a module and provides the `scrape_game_details(driver, url)` function.
    *   This function takes a Selenium WebDriver instance and a game URL as input.
    *   It navigates to the given game page and scrapes detailed attributes of the game, such as "Return to Player" (RTP), "Volatility", "Provider", and various game features (e.g., "Bonus Game", "Free Spins", "Wild Symbol").
    *   The scraped details are returned as a dictionary.

The scraper uses Selenium for web navigation and interaction, and BeautifulSoup for parsing HTML content.

## How to Run

1.  **Install dependencies:**
    Ensure you have Python installed. You'll also need to install the required libraries:
    ```bash
    pip install requests beautifulsoup4 selenium webdriver-manager pandas
    ```
    This project uses `webdriver-manager` to automatically download and manage the appropriate ChromeDriver.

2.  **Run the scraper:**
    Navigate to the `scraping/vegasslots` directory and execute the `scrape.py` script:
    ```bash
    python scrape.py
    ```
    The script will print the URL of each game page it is parsing and indicate if any failures occur during the detailed scraping process.

## Output

The scraped data is saved in a CSV file named `all_games_data.csv` in the `scraping/vegasslots` directory. Each row in the CSV represents a slot game, including its basic information and the detailed features scraped from its page.

**Note:** Web scraping can be affected by changes in the website's structure. If the scraper stops working, it might be necessary to update the selectors and parsing logic in `scrape.py` and/or `cleo.py`.
The `scrape.py` script currently only processes the first 20 games found on the main listing page. This can be adjusted by modifying the slice `slots[:20]` in the script.
