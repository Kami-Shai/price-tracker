import pandas as pd
import os
import json
import re

# ----------------- CONFIG -----------------
file_name = "price_history.csv"
output_folder = "charts"
dashboard_file = os.path.join(output_folder, "price_dashboard.html")
os.makedirs(output_folder, exist_ok=True)

# ----------------- LOAD DATA -----------------
df = pd.read_csv(file_name)
df["date"] = pd.to_datetime(df["date"])

# Clean price data - handle different formats
def clean_price(price_str):
    if pd.isna(price_str) or price_str == "Not found":
        return None
    # Remove Rs., PKR, commas, and extra spaces
    cleaned = re.sub(r'[^\d.]', '', str(price_str))
    try:
        return float(cleaned)
    except:
        return None

df["price_cleaned"] = df["price"].apply(clean_price)
df = df[df["price_cleaned"].notna()]  # Remove rows with invalid prices

books = sorted(df["book"].unique())

# ----------------- PREPARE DATA FOR JS -----------------
traces_dict = {}
for book in books:
    df_book = df[df["book"] == book].sort_values("date")
    traces_dict[book] = {
        "x": df_book["date"].dt.strftime("%Y-%m-%d").tolist(),
        "y": df_book["price_cleaned"].tolist()
    }

# ----------------- GENERATE HTML -----------------
html_content = f"""<!DOCTYPE html>
<html lang='en'>
<head>
    <meta charset='UTF-8'>
    <meta name='viewport' content='width=device-width, initial-scale=1.0'>
    <script src='https://cdn.plot.ly/plotly-2.27.0.min.js'></script>
    <title>Book Price Tracker</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Oxygen, Ubuntu, Cantarell, sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            min-height: 100vh;
            padding: 20px;
        }}
        
        .container {{
            max-width: 1400px;
            margin: 0 auto;
            background: white;
            border-radius: 16px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.3);
            overflow: hidden;
        }}
        
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 30px;
            text-align: center;
        }}
        
        .header h1 {{
            font-size: 2em;
            font-weight: 700;
            margin-bottom: 10px;
        }}
        
        .header p {{
            opacity: 0.9;
            font-size: 1.1em;
        }}
        
        .controls {{
            padding: 25px 30px;
            background: #f8f9fa;
            border-bottom: 1px solid #e9ecef;
        }}
        
        .select-wrapper {{
            position: relative;
            max-width: 600px;
            margin: 0 auto;
        }}
        
        .select-wrapper label {{
            display: block;
            margin-bottom: 10px;
            font-weight: 600;
            color: #495057;
            font-size: 0.95em;
        }}
        
        #book_select {{
            width: 100%;
            padding: 14px 40px 14px 16px;
            font-size: 16px;
            border: 2px solid #dee2e6;
            border-radius: 8px;
            background: white;
            cursor: pointer;
            appearance: none;
            transition: all 0.3s ease;
            color: #212529;
        }}
        
        #book_select:hover {{
            border-color: #667eea;
        }}
        
        #book_select:focus {{
            outline: none;
            border-color: #667eea;
            box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
        }}
        
        .select-wrapper::after {{
            content: '▼';
            position: absolute;
            right: 16px;
            top: 50%;
            transform: translateY(-50%);
            pointer-events: none;
            color: #667eea;
            font-size: 12px;
            margin-top: 12px;
        }}
        
        .chart-container {{
            padding: 30px;
        }}
        
        #chart {{
            width: 100%;
            height: 600px;
        }}
        
        .stats {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            padding: 25px 30px;
            background: #f8f9fa;
            border-top: 1px solid #e9ecef;
        }}
        
        .stat-card {{
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            text-align: center;
        }}
        
        .stat-label {{
            color: #6c757d;
            font-size: 0.85em;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 8px;
        }}
        
        .stat-value {{
            color: #212529;
            font-size: 1.5em;
            font-weight: 700;
        }}
        
        .price-change {{
            font-size: 0.9em;
            margin-top: 5px;
        }}
        
        .price-up {{
            color: #dc3545;
        }}
        
        .price-down {{
            color: #28a745;
        }}
        
        @media (max-width: 768px) {{
            body {{
                padding: 10px;
            }}
            
            .header h1 {{
                font-size: 1.5em;
            }}
            
            .header p {{
                font-size: 0.95em;
            }}
            
            .controls, .chart-container, .stats {{
                padding: 20px;
            }}
            
            #chart {{
                height: 400px;
            }}
            
            .stats {{
                grid-template-columns: 1fr;
            }}
        }}
    </style>
</head>
<body>
    <div class='container'>
        <div class='header'>
            <h1>📚 Book Price Tracker</h1>
            <p>Track price history for your favorite comic books and novels</p>
        </div>
        
        <div class='controls'>
            <div class='select-wrapper'>
                <label for='book_select'>Select a book to view price history:</label>
                <select id='book_select'>
"""

# Add book options
for book in books:
    html_content += f"                    <option value='{book}'>{book}</option>\n"

html_content += """                </select>
            </div>
        </div>
        
        <div class='chart-container'>
            <div id='chart'></div>
        </div>
        
        <div class='stats'>
            <div class='stat-card'>
                <div class='stat-label'>Current Price</div>
                <div class='stat-value' id='current-price'>-</div>
            </div>
            <div class='stat-card'>
                <div class='stat-label'>Lowest Price</div>
                <div class='stat-value' id='lowest-price'>-</div>
            </div>
            <div class='stat-card'>
                <div class='stat-label'>Highest Price</div>
                <div class='stat-value' id='highest-price'>-</div>
            </div>
            <div class='stat-card'>
                <div class='stat-label'>Price Change</div>
                <div class='stat-value' id='price-change'>-</div>
            </div>
        </div>
    </div>
    
    <script>
        const traces = """ + json.dumps(traces_dict, indent=12) + """;
        
        const select = document.getElementById('book_select');
        const chartDiv = document.getElementById('chart');
        
        function updateStats(book) {
            const data = traces[book];
            if (!data || !data.y || data.y.length === 0) return;
            
            const prices = data.y;
            const current = prices[prices.length - 1];
            const lowest = Math.min(...prices);
            const highest = Math.max(...prices);
            const first = prices[0];
            const change = current - first;
            const changePercent = ((change / first) * 100).toFixed(1);
            
            document.getElementById('current-price').textContent = `Rs. ${current.toLocaleString()}`;
            document.getElementById('lowest-price').textContent = `Rs. ${lowest.toLocaleString()}`;
            document.getElementById('highest-price').textContent = `Rs. ${highest.toLocaleString()}`;
            
            const changeEl = document.getElementById('price-change');
            const changeClass = change > 0 ? 'price-up' : 'price-down';
            const changeSymbol = change > 0 ? '↑' : '↓';
            changeEl.innerHTML = `<span class="${changeClass}">${changeSymbol} Rs. ${Math.abs(change).toLocaleString()} (${Math.abs(changePercent)}%)</span>`;
        }
        
        function plotBook(book) {
            const data = traces[book];
            
            const trace = {
                x: data.x,
                y: data.y,
                type: 'scatter',
                mode: 'lines+markers',
                line: {
                    color: '#667eea',
                    width: 3,
                    shape: 'spline'
                },
                marker: {
                    color: '#667eea',
                    size: 8,
                    line: {
                        color: 'white',
                        width: 2
                    }
                },
                fill: 'tozeroy',
                fillcolor: 'rgba(102, 126, 234, 0.1)',
                hovertemplate: '<b>%{x}</b><br>Price: Rs. %{y:,.0f}<extra></extra>'
            };
            
            const layout = {
                title: {
                    text: book,
                    font: {
                        size: 18,
                        color: '#212529',
                        family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif'
                    }
                },
                xaxis: {
                    title: 'Date',
                    tickformat: '%b %d, %Y',
                    gridcolor: '#e9ecef',
                    showgrid: true
                },
                yaxis: {
                    title: 'Price (Rs.)',
                    tickformat: ',.0f',
                    gridcolor: '#e9ecef',
                    showgrid: true
                },
                plot_bgcolor: '#ffffff',
                paper_bgcolor: '#ffffff',
                hovermode: 'x unified',
                margin: {t: 80, b: 60, l: 80, r: 40},
                font: {
                    family: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif',
                    color: '#212529'
                }
            };
            
            const config = {
                responsive: true,
                displayModeBar: true,
                displaylogo: false,
                modeBarButtonsToRemove: ['pan2d', 'lasso2d', 'select2d']
            };
            
            Plotly.react(chartDiv, [trace], layout, config);
            updateStats(book);
        }
        
        // Initial plot
        plotBook(select.value);
        
        // Update on selection
        select.addEventListener('change', () => {
            plotBook(select.value);
        });
        
        // Handle window resize
        window.addEventListener('resize', () => {
            Plotly.Plots.resize(chartDiv);
        });
    </script>
</body>
</html>"""

# Write HTML file
with open(dashboard_file, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"✅ Dashboard generated successfully: {dashboard_file}")
print(f"📊 Tracking {len(books)} books with {len(df)} total price records")
