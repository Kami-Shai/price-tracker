import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os

file_name = "price_history.csv"
output_folder = "charts"
dashboard_file = os.path.join(output_folder, "price_dashboard.html")

os.makedirs(output_folder, exist_ok=True)

# Load CSV
df = pd.read_csv(file_name)
df["date"] = pd.to_datetime(df["date"])
df["price"] = df["price"].str.replace("Rs.", "").str.replace(",", "").astype(float)

# Get unique books
books = df["book"].unique()

# Create subplots: one row per book
fig = make_subplots(
    rows=len(books), cols=1,
    shared_xaxes=False,
    subplot_titles=books,
    vertical_spacing=0.05
)

# Add a line for each book
for i, book in enumerate(books, start=1):
    df_book = df[df["book"] == book].sort_values("date")
    fig.add_trace(
        go.Scatter(
            x=df_book["date"],
            y=df_book["price"],
            mode="lines+markers",
            name=book,
            hovertemplate="%{x|%b %d, %Y}<br>Price: Rs.%{y}<extra></extra>"
        ),
        row=i, col=1
    )

# Layout
fig.update_layout(
    height=300 * len(books),  # Adjust height for number of books
    title_text="Book Price History Dashboard",
    showlegend=False,
    template="plotly_white"
)

# Update x-axes to monthly ticks
for i in range(1, len(books)+1):
    fig.update_xaxes(tickformat="%b\n%Y", dtick="M1", row=i, col=1)
    fig.update_yaxes(title_text="Price (Rs.)", row=i, col=1)

# Save dashboard
fig.write_html(dashboard_file)
print(f"✅ Dashboard saved: {dashboard_file}")
