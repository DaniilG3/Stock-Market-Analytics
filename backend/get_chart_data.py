import psycopg2
import json

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="stock_data",
    user="daniilgoncharuk",  # change if needed
    host="localhost"
)
cursor = conn.cursor()

# Change 'AAPL' to any symbol you'd like
symbol = 'AAPL'

cursor.execute("""
    SELECT timestamp::time, close, sma_5
    FROM stocks
    WHERE symbol = %s AND sma_5 IS NOT NULL
    ORDER BY timestamp DESC
    LIMIT 10
""", (symbol,))

rows = cursor.fetchall()

# Reverse to show oldest -> newest
rows.reverse()

# Convert to chart-friendly format
chart_data = [
    {"timestamp": row[0].strftime("%H:%M"), "close": float(row[1]), "sma_5": float(row[2])}
    for row in rows
]

print(json.dumps(chart_data, indent=2))

