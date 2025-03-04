# pip install selenium webdriver-manager pandas (To install dependencies)

import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager

def setup_driver():
    """Sets up Selenium WebDriver for Chrome."""
    chrome_options = Options()
    chrome_options.add_argument("--start-maximized")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-extensions")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")

    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    return driver

def scrape_google_results(query, num_results=10):
    """Scrapes Google search results for a given query."""
    base_url = "https://www.google.com/search?q=" + query.replace(" ", "+")
    driver = setup_driver()
    driver.get(base_url)

    try:
        # Wait for search results to load
        WebDriverWait(driver, 10).until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, "div.g")))
        
        search_results = driver.find_elements(By.CSS_SELECTOR, "div.g")
        scraped_data = []

        for result in search_results[:num_results]:
            try:
                title = result.find_element(By.TAG_NAME, "h3").text
                link = result.find_element(By.TAG_NAME, "a").get_attribute("href")
                snippet = result.find_element(By.CSS_SELECTOR, "div.VwiC3b").text if result.find_elements(By.CSS_SELECTOR, "div.VwiC3b") else "No snippet available"
                
                scraped_data.append({"Title": title, "Link": link, "Snippet": snippet})

            except NoSuchElementException:
                continue

    except TimeoutException:
        print("Timeout: Google search results did not load in time.")
        scraped_data = []

    driver.quit()
    return scraped_data

def save_to_csv(data, filename="google_results.csv"):
    """Saves scraped data to a CSV file."""
    if data:
        df = pd.DataFrame(data)
        df.to_csv(filename, index=False, encoding='utf-8')
        print(f"Results saved to {filename}")
    else:
        print("No results to save.")

if __name__ == "__main__":
    query = input("Enter your search query: ").strip()
    results = scrape_google_results(query)
    
    if results:
        save_to_csv(results)
    else:
        print("No results found.")



# How This Works:
# Sets up Selenium WebDriver for Chrome using webdriver-manager.
# Searches Google for a given query and waits for results to load.
# Extracts the title, URL, and snippet of each search result.
# Saves the results in a CSV file (google_results.csv).
# Handles errors gracefully (timeouts, missing elements).
