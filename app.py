from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from datetime import datetime
import time

# Set up Chrome options
options = Options()
options.add_argument('--ignore-certificate-errors')  # Ignore SSL warnings
options.add_argument('--disable-gpu')  # Disable GPU acceleration
options.add_argument('--headless')  # Run Chrome in headless mode (optional)
options.add_argument('--no-sandbox')  # Helps with running in some environments
options.add_argument('--disable-dev-shm-usage')  # Prevents crashes in Docker/Linux
options.add_argument('--enable-unsafe-swiftshader')  # For WebGL deprecation warnings

# Set up ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Base URL for scraping
base_url = "https://stock.adobe.com/vn/search?creator_id=209261008&filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bcontent_type%3Aaudio%5D=0&filters%5Binclude_stock_enterprise%5D=0&filters%5Bis_editorial%5D=0&filters%5Bfetch_excluded_assets%5D=1&filters%5Bcontent_type%3Aimage%5D=1&order=relevance&search_page=2&get_facets=0&search_type=pagination"
# Function to scrape titles from a page
def scrape_page(url):
    try:
        driver.get(url)
        time.sleep(5)  # Wait for page load
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        titles = soup.find_all('meta', itemprop='name')
        return [title.get('content', '').strip() for title in titles]
    except Exception as e:
        print(f"Error scraping page: {e}")
        return []

# Function to get all pages
def get_all_pages(start_page, end_page):
    titles = []
    for page in range(start_page, end_page + 1):
        url = f"{base_url}&search_page={page}"
        print(f"Scraping page {page}: {url}")
        page_titles = scrape_page(url)
        titles.extend(page_titles)
        time.sleep(1)  # Avoid overwhelming the server
    return titles

# Scrape from page 10 to page 20 and save to a text file
start_page = 1 
end_page = 10
all_titles = get_all_pages(start_page, end_page)

# Generate filename with date and time
current_datetime = datetime.now()
filename = f"{current_datetime.day:02d}{current_datetime.month:02d}{current_datetime.year}{current_datetime.hour:02d}{current_datetime.minute:02d}{current_datetime.second:02d}.txt"

# Export to a text file
with open(filename, 'w', encoding='utf-8') as file:
    for title in all_titles:
        file.write(title + '\n')

print(f"Scraping completed. Data saved to {filename}")

# Close the browser
driver.quit()
