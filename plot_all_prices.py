import pandas as pd
import matplotlib.pyplot as plt
import os

file_name = "price_history.csv"
output_folder = "charts"

# Ensure folder exists
os.makedirs(output_folder, exist_ok=True)

# Load CSV
df = pd.read_csv(file_name)
df["date"] = pd.to_datetime(df["date"])

# Clean price column
df["price"] = df["price"].str.replace("Rs.", "").str.replace(",", "").astype(float)

# Get unique books
books = df["book"].unique()

for book in books:
    df_book = df[df["book"] == book].sort_values("date")

    plt.figure(figsize=(10,5))
    plt.plot(df_book["date"], df_book["price"], marker="o", linestyle="-", color="blue")
    plt.title(f"Price History: {book}")
    plt.xlabel("Date")
    plt.ylabel("Price (Rs.)")
    plt.grid(True)
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Safe filename
    safe_name = "".join(c for c in book if c.isalnum() or c in (" ", "_")).rstrip()
    file_path = os.path.join(output_folder, f"{safe_name[:30]}_chart.png")
    plt.savefig(file_path)
    plt.close()
    print(f"✅ Chart saved: {file_path}")
