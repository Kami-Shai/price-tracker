import pandas as pd
import os
import json

# ----------------- CONFIG -----------------
file_name = "price_history.csv"
output_folder = "charts"
dashboard_file = os.path.join(output_folder, "price_dashboard.html")

os.makedirs(output_folder, exist_ok=True)

# ----------------- LOAD DATA -----------------
df = pd.read_csv(file_name)
df["date"] = pd.to_datetime(df["date"])
df["price"] = df["price"].str.replace("Rs.", "").str.replace(",", "").astype(float)

books = df["book"].unique()

# ----------------- PREPARE DATA FOR JS -----------------
traces_dict = {}
for book in books:
    df_book = df[df["book"] == book].sort_values("date")
    traces_dict[book] = {
        "x": json.dumps(df_book["date"].dt.strftime("%Y-%m-%d").tolist()),  # convert dates to strings
        "y": json.dumps(df_book["price"].tolist())
    }

# ----------------- GENERATE HTML -----------------
html_lines = [
    "<!DOCTYPE html>",
    "<html lang='en'>",
    "<head>",
    "  <meta charset='UTF-8'>",
    "  <meta name='viewport' content='width=device-width, initial-scale=1.0'>",
    "  <script src='https://cdn.plot.ly/plotly-latest.min.js'></script>",
    "  <title>Book Price Dashboard</title>",
    "  <style> body{ font-family: Arial; padding: 10px;} </style>",
    "</head>",
    "<body>",
    "  <h2>Book Price History Dashboard</h2>",
    "  <label for='book_select'>Select Book:</label>",
    "  <select id='book_select'>"
]

# Add book options
for book in books:
    html_lines.append(f"    <option value='{book}'>{book}</option>")

html_lines.extend([
    "  </select>",
    "  <div id='chart' style='width:100%;height:600px;'></div>",
    "  <script>",
    "    const traces = {"
])

# Add JS traces
for book in books:
    html_lines.append(f"      '{book}': {{ x: {traces_dict[book]['x']}, y: {traces_dict[book]['y']} }},")
html_lines.append("    };")

# JS to plot and update
html_lines.extend([
"""
    const select = document.getElementById('book_select');
    const chartDiv = document.getElementById('chart');

    function plotBook(book) {
        const data = [{
            x: traces[book].x,
            y: traces[book].y,
            type: 'scatter',
            mode: 'lines+markers',
            marker: {color: '#1f77b4'},
            hovertemplate: '%{x}<br>Price: Rs.%{y}<extra></extra>'
        }];
        const layout = {
            title: `Price History: ${book}`,
            margin: {t:80,b:50,l:60,r:50},
            xaxis: {title: 'Date', tickformat:'%b %Y'},
            yaxis: {title: 'Price (Rs.)'},
            hovermode: 'closest',
            template: 'plotly_white',
            autosize: true
        };
        Plotly.react(chartDiv, data, layout, {responsive:true});
    }

    // Initial plot
    plotBook(select.value);

    // Update on selection
    select.addEventListener('change', () => {
        plotBook(select.value);
    });
"""
])

html_lines.extend([
    "  </script>",
    "</body>",
    "</html>"
])

# Write HTML file
with open(dashboard_file, "w", encoding="utf-8") as f:
    f.write("\n".join(html_lines))

print(f"✅ Mobile and desktop-friendly dashboard saved: {dashboard_file}")
