import pandas as pd
import plotly.graph_objects as go
import os

file_name = "price_history.csv"
output_folder = "charts"
dashboard_file = os.path.join(output_folder, "price_dashboard.html")

os.makedirs(output_folder, exist_ok=True)

# Load CSV
df = pd.read_csv(file_name)
df["date"] = pd.to_datetime(df["date"])
df["price"] = df["price"].str.replace("Rs.", "").str.replace(",", "").astype(float)

# Unique books
books = df["book"].unique()

# Create figure
fig = go.Figure()

# Add a trace for each book (only first visible initially)
for i, book in enumerate(books):
    df_book = df[df["book"] == book].sort_values("date")
    fig.add_trace(
        go.Scatter(
            x=df_book["date"],
            y=df_book["price"],
            mode="lines+markers",
            name=book,
            hovertemplate="%{x|%b %d, %Y}<br>Price: Rs.%{y}<extra></extra>",
            visible=(i == 0)
        )
    )

# Create dropdown buttons
buttons = []
for i, book in enumerate(books):
    visibility = [False] * len(books)
    visibility[i] = True
    buttons.append(
        dict(
            label=book,
            method="update",
            args=[{"visible": visibility},
                  {"title": f"Price History: {book}"}]
