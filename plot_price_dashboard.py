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

# Add a trace for each book (initially visible=False except the first)
for i, book in enumerate(books):
    df_book = df[df["book"] == book].sort_values("date")
    fig.add_trace(
        go.Scatter(
            x=df_book["date"],
            y=df_book["price"],
            mode="lines+markers",
            name=book,
            hovertemplate="%{x|%b %d, %Y}<br>Price: Rs.%{y}<extra></extra>",
            visible=(i == 0)  # Only first book visible initially
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
        )
    )

fig.update_layout(
    updatemenus=[dict(
        active=0,
        buttons=buttons,
        x=0.05,
        y=1.15,
        xanchor="left",
        yanchor="top"
    )],
    title=f"Price History: {books[0]}",
    xaxis=dict(tickformat="%b\n%Y"),
    yaxis=dict(title="Price (Rs.)"),
    hovermode="closest",
    template="plotly_white",
    width=1200,
    height=700
)

# Save HTML dashboard
fig.write_html(dashboard_file)
print(f"✅ Dashboard saved: {dashboard_file}")
