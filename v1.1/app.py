from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time
import random
import string
from datetime import datetime

# Generate random 8-character prefix
def generate_random_prefix():
    prefix = "p" + ''.join(random.choice(string.digits) for _ in range(7))
    return prefix

# Set up Chrome options
options = Options()
options.add_argument('--ignore-certificate-errors')
options.add_argument('--disable-gpu')
options.add_argument('--headless')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')
options.add_argument('--enable-unsafe-swiftshader')

# Set up ChromeDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)

# Base URL for scraping
base_url = "https://stock.adobe.com/vn/search?creator_id=206854500&filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bcontent_type%3Aaudio%5D=0&filters%5Binclude_stock_enterprise%5D=0&filters%5Bis_editorial%5D=0&filters%5Bfetch_excluded_assets%5D=1&filters%5Bcontent_type%3Aimage%5D=1&order=relevance&get_facets=0&search_type=pagination"

# Custom text to append
custom_text = "dumnaf"
aspect_ratio = "16:9"
additional_params = "--no dust --p 5y3izqx"

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

# Function to get all pages and format prompts with duplicate removal
def get_all_pages(start_page, end_page):
    all_titles = []
    
    # Collect all titles first
    for page in range(start_page, end_page + 1):
        url = f"{base_url}&search_page={page}"
        print(f"Scraping page {page}: {url}")
        page_titles = scrape_page(url)
        all_titles.extend(page_titles)
        time.sleep(1)  # Avoid overwhelming the server
    
    # Remove duplicates while preserving order
    unique_titles = list(dict.fromkeys(all_titles))
    
    # Format prompts with prefix, numbering, and suffix
    formatted_prompts = []
    prefix = generate_random_prefix()
    current_date = datetime.now().strftime('%d%m%Y')
    
    for count, title in enumerate(unique_titles, 1):
        if title:
            formatted_prompt = f"{prefix} {count:02d} {title} {current_date}{custom_text} {additional_params} --ar {aspect_ratio}"
            formatted_prompts.append(formatted_prompt)
            
    return formatted_prompts

# Scrape pages 1 to 10 and save to a text file
start_page = 1
end_page = 10
all_prompts = get_all_pages(start_page, end_page)

# Generate filename with date and time
current_datetime = datetime.now()
filename = f"{current_datetime.day:02d}{current_datetime.month:02d}{current_datetime.year}{current_datetime.hour:02d}{current_datetime.minute:02d}{current_datetime.second:02d}tic.txt"

# Export to a text file
with open(filename, 'w', encoding='utf-8') as file:
    for prompt in all_prompts:
        file.write(prompt + '\n')

print(f"Scraping completed. Data saved to {filename}")

# Close the browser
driver.quit()
