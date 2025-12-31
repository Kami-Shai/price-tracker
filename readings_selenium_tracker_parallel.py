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
    "Thor By Jason Aaron Omnibus (Volume 2)": "https://readings.com.pk/book/1646685?srsltid=...",
    "Wolverine By Jason Aaron Omnibus Vol. 1 David Finch Cover [New Printing]": "https://readings.com.pk/book/1890468",
    "Wolverine Goes To Hell Omnibus Jae Lee Cover [New Printing]": "https://readings.com.pk/book/1890517",
    "Thor By Straczynski & Gillen Omnibus": "https://www.readings.com.pk/book/1755329",
    "Loki: God Of Stories Omnibus": "https://www.readings.com.pk/book/1755412",
    "Lucifer Omnibus Vol. 1 (The Sandman Universe Classics)": "https://www.readings.com.pk/book/1759230",
    "Lucifer Omnibus Vol. 2 (The Sandman Universe Classics)": "https://www.readings.com.pk/book/1758950",
    "The Planetary Omnibus": "https://www.readings.com.pk/book/1441716",
    "Death: The Deluxe Edition (2022 Edition)": "https://www.readings.com.pk/book/1548649",
    "Batman By Paul Dini Omnibus (New Edition)": "https://www.readings.com.pk/book/1758841",
    "Absolute Superman For All Seasons": "https://www.readings.com.pk/book/1758926",
    "Gotham Central Omnibus (2022 Edition)": "https://www.readings.com.pk/book/1758872",
    "The Animal Man Omnibus (2022 Edition)": "https://www.readings.com.pk/book/1758617",
    "Absolute Kingdom Come (New Edition)": "https://www.readings.com.pk/book/1422939",
    "Alice In Borderland (Volume 1)": "https://www.readings.com.pk/book/1372404",
    "Alice In Borderland (Volume 2)": "https://www.readings.com.pk/book/1375809",
    "Alice In Borderland (Volume 3)": "https://www.readings.com.pk/book/1556304",
    "Alice In Borderland (Volume 4)": "https://www.readings.com.pk/book/1603961",
    "Alice In Borderland (Volume 5)": "https://www.readings.com.pk/book/1626925",
    "Alice In Borderland, Vol. 6": "https://www.readings.com.pk/book/1884195",
    "Alice In Borderland, Vol. 7": "https://www.readings.com.pk/book/1856730",
    "Alice In Borderland, Vol. 8": "https://www.readings.com.pk/book/1857183",
    "Alice In Borderland, Vol. 9": "https://www.readings.com.pk/book/1851369",
    "Noel: Batman (Volume 1)": "https://www.readings.com.pk/book/1546799",
    "The Count Of Monte Cristo (Penguin Clothbound Classics)": "https://www.readings.com.pk/book/1533993",
    "Superior Spider-Man Omnibus Vol. 1": "https://www.readings.com.pk/book/1754005",
    "Doctor Strange By Jed Mackay Omnibus": "https://www.readings.com.pk/book/1952246",
    "Hawkeye By Fraction & Aja Omnibus [New Printing]": "https://www.readings.com.pk/book/1753984",
    "Batman: Omnibus (Volume 1)": "https://www.readings.com.pk/book/1489875",
    "Batman By Jeph Loeb & Tim Sale Omnibus": "https://www.readings.com.pk/book/1758865",
    "Batman: Hush 20th Anniversary Edition (Volume 58)": "https://www.readings.com.pk/book/1565542",
    "Absolute Justice League: The World’S Greatest Super‑Heroes By Alex Ross & Paul Dini (New Edition)": "https://www.readings.com.pk/book/1759085",
    "Absolute DC: The New Frontier (2025 Edition)": "https://www.readings.com.pk/book/1890113",
    "Superman By Kurt Busiek Book One": "https://www.readings.com.pk/book/1758974",
    "Superman By Kurt Busiek Book Two": "https://www.readings.com.pk/book/1890061",
    "Superman: Birthright The Deluxe Edition (Volume 1)": "https://www.readings.com.pk/book/1591552",
    "Vision: The Complete Collection": "https://www.readings.com.pk/book/1754915",
    "Spider-Man By Chip Zdarsky Omnibus": "https://www.readings.com.pk/book/1754067",
    "The Batman Who Laughs": "https://www.readings.com.pk/book/1424532",
    "Superman Smashes The Klan": "https://www.readings.com.pk/book/1759089",
    "Batman By Darwyn Cooke: Absolute Edition": "https://www.readings.com.pk/book/1963899",
    "Green Lantern: Earth One (Volume 1)": "https://www.readings.com.pk/book/1438883"
}

file_name = "price_history.csv"
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
rows = []

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

# ----------------- OPEN ALL BOOKS IN TABS -----------------
tabs = []
for idx, (name, url) in enumerate(books.items()):
    if idx == 0:
        driver.get(url)
        tabs.append(driver.current_window_handle)
    else:
        driver.execute_script("window.open('{}');".format(url))
        tabs.append(driver.window_handles[-1])

# ----------------- SCRAPE -----------------
for tab, (name, _) in zip(tabs, books.items()):
    driver.switch_to.window(tab)
    try:
        price_elem = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "span.sale-price"))
        )
        price = price_elem.text.strip().replace("\n", "")
        print(f"✔ {name}: {price}")
    except Exception as e:
        price = "Not found"
        print(f"❌ {name}: Failed to scrape.")
    rows.append({"date": timestamp, "book": name, "price": price})

driver.quit()

# ----------------- SAVE CSV -----------------
df_new = pd.DataFrame(rows)
if os.path.exists(file_name) and os.path.getsize(file_name) > 0:
    df_existing = pd.read_csv(file_name)
    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["book", "date"])
    df_combined.to_csv(file_name, index=False)
else:
    df_new.to_csv(file_name, index=False)

print("\n✅ Done. Prices saved to", file_name)
