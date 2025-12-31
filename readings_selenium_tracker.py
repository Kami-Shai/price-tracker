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
    "Thor By Jason Aaron Omnibus (Volume 1)": "https://readings.com.pk/book/1646684",
    "Thor By Jason Aaron Omnibus (Volume 2)": "https://readings.com.pk/book/1646685?srsltid=AfmBOoqp7eWOqFk11FZcN3gTqBRAdO-apBPXj6wUPI6AtOXTV8vt8zsp",
    # ... (all other 44 books) ...
}

file_name = "price_history.csv"
log_file = "scraper_errors.log"

# ----------------- SETUP CHROME -----------------
options = Options()
options.add_argument("--headless")
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--window-size=1920,1080")

driver = webdriver.Chrome(
    service=Service(ChromeDriverManager().install()),
    options=options
)

rows = []

# ----------------- SCRAPE PRICES WITH RETRY AND LOGGING -----------------
MAX_RETRIES = 3
RETRY_DELAY = 5  # seconds

for name, url in books.items():
    for attempt in range(1, MAX_RETRIES + 1):
        try:
            driver.get(url)
            price_elem = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "span.sale-price"))
            )
            price = price_elem.text.strip().replace("\n", "")
            break  # success
        except Exception as e:
            price = "Not found"
            if attempt == MAX_RETRIES:
                # Log the failure
                with open(log_file, "a", encoding="utf-8") as f:
                    f.write(f"{datetime.now().strftime('%Y-%m-%d %H:%M')} | {name} | {url} | {e}\n")
                print(f"❌ Failed to fetch {name} after {MAX_RETRIES} attempts. Logged.")
            else:
                print(f"⚠️ Attempt {attempt} failed for {name}, retrying in {RETRY_DELAY}s...")
                time.sleep(RETRY_DELAY)

    rows.append({
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
        "book": name,
        "price": price
    })

    print(f"✔ {name}: {price}")

driver.quit()

# ----------------- SAVE TO CSV -----------------
df_new = pd.DataFrame(rows)

if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
    df_existing = pd.read_csv(file_name)
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["book", "date"])
    df_combined.to_csv(file_name, index=False)
else:
    df_new.to_csv(file_name, index=False)

print("\n✅ Done. Prices saved to", file_name)
print(f"🔹 Any failures logged to {log_file}")
