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

# ----------------- CONFIG -----------------
books = {
    "Superman: The Last Days of Lex Luthor": "https://www.readings.com.pk/book/1890067",
    # Add more books here
}

file_name = "price_history.csv"

# ----------------- SETUP CHROME -----------------
options = Options()
options.add_argument("--headless")  # Remove if you want to see the browser
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

if os.path.exists(file_name):
    df_existing = pd.read_csv(file_name)
    # Combine and drop duplicates based on book and date
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["book", "date"])
    df_combined.to_csv(file_name, index=False)
else:
    df_new.to_csv(file_name, index=False)

print("\n✅ Done. Prices saved to", file_name)