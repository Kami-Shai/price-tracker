import pandas as pd
import plotly.express as px
import os

file_name = "price_history.csv"
output_folder = "charts"

# Ensure output folder exists
os.makedirs(output_folder, exist_ok=True)

# Load CSV
df = pd.read_csv(file_name)
df["date"] = pd.to_datetime(df["date"])

# Clean price column
df["price"] = df["price"].str.replace("Rs.", "").str.replace(",", "").astype(float)

# Unique books
books = df["book"].unique()

for book in books:
    df_book = df[df["book"] == book].sort_values("date")
    
    # Interactive line chart
    fig = px.line(
        df_book,
        x="date",
        y="price",
        title=f"Price History: {book}",
        labels={"price": "Price (Rs.)", "date": "Date"},
        markers=True,
        hover_data={"price": True, "date": True}
    )

    # Set x-axis ticks to monthly intervals
    fig.update_xaxes(
        dtick="M1",
        tickformat="%b\n%Y"
    )

    # Save interactive HTML file
    safe_name = "".join(c for c in book if c.isalnum() or c in (" ", "_")).rstrip()
    file_path = os.path.join(output_folder, f"{safe_name[:30]}_chart.html")
    fig.write_html(file_path)
    print(f"✅ Interactive chart saved: {file_path}")
