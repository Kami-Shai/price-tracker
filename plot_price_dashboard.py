import pandas as pd
import plotly.graph_objects as go
import os

file_name = "price_history.csv"
output_folder = "charts"
dashboard_file = os.path.join(output_folder, "price_dashboard.html")

os.makedirs(output_folder, exist_ok=True)

# Load data
df = pd.read_csv(file_name)
df["date"] = pd.to_datetime(df["date"])
df["price"] = df["price"].str.replace("Rs.", "").str.replace(",", "").astype(float)

# Unique books
books = df["book"].unique()

# Create a figure with one trace per book
fig = go.Figure()

for book in books:
    df_book = df[df["book"] == book].sort_values("date")
    fig.add_trace(
        go.Scatter(
            x=df_book["date"],
            y=df_book["price"],
            mode="lines+markers",
            name=book,
            hovertemplate="%{x|%b %d, %Y}<br>Price: Rs.%{y}<extra></extra>"
        )
    )

# Update layout
fig.update_layout(
    title="Book Price History Dashboard",
    xaxis_title="Date",
    yaxis_title="Price (Rs.)",
    xaxis=dict(
        tickformat="%b\n%Y",
        dtick="M1"
    ),
    hovermode="closest",
    legend_title="Books",
    template="plotly_white",
    width=1200,
    height=700
)

# Save dashboard as HTML
fig.write_html(dashboard_file)
print(f"✅ Dashboard saved: {dashboard_file}")
