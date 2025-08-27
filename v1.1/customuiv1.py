import tkinter as tk
from tkinter import ttk, scrolledtext
import random
import string
from datetime import datetime
import logging
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import time

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("scraper.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

def generate_random_prefix():
    prefix = "p" + ''.join(random.choice(string.digits) for _ in range(7))
    logger.info(f"Generated random prefix: {prefix}")
    return prefix

def update_preview():
    # Get values from UI
    prefix = prefix_entry.get() or generate_random_prefix()
    custom_suffix = custom_suffix_entry.get() or "dumnaf"
    aspect_ratio = aspect_ratio_var.get()
    additional_params = additional_params_entry.get() or "--no dust --p 5y3izqx"
    
    # Format current date
    current_date = datetime.now().strftime('%d%m%Y')
    
    # Create sample preview
    sample_text = "A cheerful real estate agent exhibits a spacious, empty office with large windows. The setting radiates opportunity and potential, ideal for businesses ready to move forward."
    
    preview_text = f"{prefix} 01 {sample_text} {current_date}{custom_suffix} {additional_params} --ar {aspect_ratio}"
    preview_area.delete(1.0, tk.END)
    preview_area.insert(tk.END, preview_text)
    logger.info("Preview updated")

def start_scraping():
    try:
        url = url_entry.get()
        start_page = int(start_page_entry.get())
        end_page = int(end_page_entry.get())
        custom_suffix = custom_suffix_entry.get()
        aspect_ratio = aspect_ratio_var.get()
        additional_params = additional_params_entry.get()
        base_filename = filename_entry.get() or "output"
        
        status_label.config(text=f"Scraping pages {start_page} to {end_page}...")
        log_area.insert(tk.END, f"Starting scrape from page {start_page} to {end_page}\n")
        
        # Set up Chrome options
        options = Options()
        options.add_argument('--ignore-certificate-errors')
        options.add_argument('--disable-gpu')
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--enable-unsafe-swiftshader')  # Fix for WebGL deprecation warnings
        
        log_area.insert(tk.END, "Setting up Chrome driver...\n")
        logger.info("Setting up Chrome driver")
        
        # Set up ChromeDriver
        driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        
        # Base URL for scraping
        base_url = url
        
        # Function to scrape titles from a page
        def scrape_page(url):
            try:
                log_area.insert(tk.END, f"Accessing URL: {url}\n")
                log_area.see(tk.END)
                root.update()
                
                driver.get(url)
                time.sleep(5)  # Wait for page load
                
                soup = BeautifulSoup(driver.page_source, 'html.parser')
                titles = soup.find_all('meta', itemprop='name')
                
                log_area.insert(tk.END, f"Found {len(titles)} titles on page\n")
                log_area.see(tk.END)
                root.update()
                
                return [title.get('content', '').strip() for title in titles]
            except Exception as e:
                error_msg = f"Error scraping page: {e}"
                log_area.insert(tk.END, error_msg + "\n")
                log_area.see(tk.END)
                logger.error(error_msg)
                return []
        
        # Collect all titles
        all_titles = []
        for page in range(start_page, end_page + 1):
            url = f"{base_url}&search_page={page}"
            log_area.insert(tk.END, f"Scraping page {page}: {url}\n")
            log_area.see(tk.END)
            root.update()
            
            page_titles = scrape_page(url)
            all_titles.extend(page_titles)
            time.sleep(1)  # Avoid overwhelming the server
        
        # Remove duplicates while preserving order
        log_area.insert(tk.END, f"Total titles before removing duplicates: {len(all_titles)}\n")
        unique_titles = list(dict.fromkeys(all_titles))
        log_area.insert(tk.END, f"Unique titles after removing duplicates: {len(unique_titles)}\n")
        log_area.see(tk.END)
        
        # Format prompts
        formatted_prompts = []
        prefix = prefix_entry.get() or generate_random_prefix()
        current_date = datetime.now().strftime('%d%m%Y')
        
        for count, title in enumerate(unique_titles, 1):
            if title:
                formatted_prompt = f"{prefix} {count:02d} {title} {current_date}{custom_suffix} {additional_params} --ar {aspect_ratio}"
                formatted_prompts.append(formatted_prompt)
        
        # Generate filename with date and time
        current_datetime = datetime.now()
        formatted_date = current_datetime.strftime('%d%m%Y%H%M%S')
        filename = f"{base_filename}{formatted_date}tic.txt"
        
        # Export to a text file
        log_area.insert(tk.END, f"Writing {len(formatted_prompts)} prompts to file: {filename}\n")
        with open(filename, 'w', encoding='utf-8') as file:
            for prompt in formatted_prompts:
                file.write(prompt + '\n')
        
        log_area.insert(tk.END, f"Scraping completed. Data saved to {filename}\n")
        status_label.config(text=f"Completed! Saved to {filename}")
        log_area.see(tk.END)
        
        # Close the browser
        driver.quit()
        
    except Exception as e:
        error_msg = f"Critical error: {str(e)}"
        log_area.insert(tk.END, error_msg + "\n")
        log_area.see(tk.END)
        logger.error(error_msg, exc_info=True)
        status_label.config(text="Error occurred! Check logs.")

# Create main window
root = tk.Tk()
root.title("Adobe Stock Prompt Generator")
root.geometry("900x700")

# URL input section
url_frame = ttk.LabelFrame(root, text="URL Settings")
url_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(url_frame, text="Adobe Stock URL:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
url_entry = ttk.Entry(url_frame, width=80)
url_entry.grid(row=0, column=1, padx=5, pady=5)
url_entry.insert(0, "https://stock.adobe.com/vn/search?creator_id=206854500&filters%5Bcontent_type%3Aphoto%5D=1&filters%5Bcontent_type%3Aillustration%5D=1&filters%5Bcontent_type%3Azip_vector%5D=1&filters%5Bcontent_type%3Avideo%5D=1&filters%5Bcontent_type%3Atemplate%5D=1&filters%5Bcontent_type%3A3d%5D=1&filters%5Bcontent_type%3Aaudio%5D=0&filters%5Binclude_stock_enterprise%5D=0&filters%5Bis_editorial%5D=0&filters%5Bfetch_excluded_assets%5D=1&filters%5Bcontent_type%3Aimage%5D=1&order=relevance&get_facets=0&search_type=pagination")

# Page range
ttk.Label(url_frame, text="Start Page:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
start_page_entry = ttk.Entry(url_frame, width=10)
start_page_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
start_page_entry.insert(0, "1")

ttk.Label(url_frame, text="End Page:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
end_page_entry = ttk.Entry(url_frame, width=10)
end_page_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)
end_page_entry.insert(0, "10")

# Format settings
format_frame = ttk.LabelFrame(root, text="Format Settings")
format_frame.pack(fill="x", padx=10, pady=5)

ttk.Label(format_frame, text="Prefix:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
prefix_entry = ttk.Entry(format_frame, width=20)
prefix_entry.grid(row=0, column=1, sticky="w", padx=5, pady=5)
prefix_entry.insert(0, generate_random_prefix())

ttk.Button(format_frame, text="Generate New", command=lambda: prefix_entry.delete(0, tk.END) or prefix_entry.insert(0, generate_random_prefix())).grid(row=0, column=2, padx=5, pady=5)

ttk.Label(format_frame, text="Custom Suffix:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
custom_suffix_entry = ttk.Entry(format_frame, width=20)
custom_suffix_entry.grid(row=1, column=1, sticky="w", padx=5, pady=5)
custom_suffix_entry.insert(0, "dumnaf")

ttk.Label(format_frame, text="Aspect Ratio:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
aspect_ratio_var = tk.StringVar(value="16:9")
aspect_ratio_combo = ttk.Combobox(format_frame, textvariable=aspect_ratio_var, values=["16:9", "4:3", "1:1", "9:16"])
aspect_ratio_combo.grid(row=2, column=1, sticky="w", padx=5, pady=5)

ttk.Label(format_frame, text="Additional Parameters:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
additional_params_entry = ttk.Entry(format_frame, width=40)
additional_params_entry.grid(row=3, column=1, columnspan=2, sticky="w", padx=5, pady=5)
additional_params_entry.insert(0, "--no dust --p 5y3izqx")

ttk.Label(format_frame, text="Output Filename:").grid(row=4, column=0, sticky="w", padx=5, pady=5)
filename_entry = ttk.Entry(format_frame, width=20)
filename_entry.grid(row=4, column=1, sticky="w", padx=5, pady=5)
filename_entry.insert(0, "output")

# Preview section
preview_frame = ttk.LabelFrame(root, text="Preview")
preview_frame.pack(fill="x", padx=10, pady=5)

preview_area = scrolledtext.ScrolledText(preview_frame, wrap=tk.WORD, height=5)
preview_area.pack(fill="both", expand=True, padx=5, pady=5)

# Log section
log_frame = ttk.LabelFrame(root, text="Log")
log_frame.pack(fill="both", expand=True, padx=10, pady=5)

log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, height=10)
log_area.pack(fill="both", expand=True, padx=5, pady=5)

# Buttons
button_frame = ttk.Frame(root)
button_frame.pack(fill="x", padx=10, pady=5)

ttk.Button(button_frame, text="Update Preview", command=update_preview).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Start Scraping", command=start_scraping).pack(side=tk.LEFT, padx=5)
ttk.Button(button_frame, text="Clear Log", command=lambda: log_area.delete(1.0, tk.END)).pack(side=tk.LEFT, padx=5)

# Status label
status_label = ttk.Label(root, text="Ready to scrape")
status_label.pack(padx=10, pady=5)

# Initialize preview
update_preview()

root.mainloop()
