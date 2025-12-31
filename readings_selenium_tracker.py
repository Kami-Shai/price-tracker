from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime
import pandas as pd
import os
import time

# ----------------- CONFIG -----------------
books = {
    "Superman: The Last Days of Lex Luthor": "https://www.readings.com.pk/book/1890067",
    # Add more books here
}

file_name = "price_history.csv"

# ----------------- SETUP CHROME -----------------
options = Options()
options.add_argument("--headless")   # Runs without opening a browser window
options.add_argument("--no-sandbox") # Required in some Linux cloud runners
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

rows = []

# ----------------- SCRAPE PRICES -----------------
for name, url in books.items():
    driver.get(url)
    
    try:
        price_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.sale-price"))
        )
        price = price_elem.text.strip().replace("\n", "")
    except:
        price = "Not found"
    
    rows.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "book": name,
        "price": price
    })
    
    print(f"✔ {name}: {price}")

driver.quit()

# ----------------- SAVE TO CSV -----------------
df_new = pd.DataFrame(rows)

# Check if CSV exists and is not empty
if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
    df_existing = pd.read_csv(file_name)
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["book", "date"])
    df_combined.to_
