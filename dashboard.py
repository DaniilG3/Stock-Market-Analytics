import streamlit as st
import pandas as pd
import psycopg2

# Page title
st.title("📈 Real-Time Stock Dashboard")

# Dropdown to select stock symbol
selected_symbol = st.selectbox("Choose a stock symbol:", ["AAPL", "TSLA", "AMZN", "MSFT", "GOOG"])

# Connect to PostgreSQL
conn = psycopg2.connect(
    dbname="stock_data",
    user="daniilgoncharuk",
    host="localhost"
)
cursor = conn.cursor()

# Query data for selected symbol
query = """
    SELECT timestamp, close, sma_5
    FROM stocks
    WHERE symbol = %s
    ORDER BY timestamp ASC
"""
cursor.execute(query, (selected_symbol,))
rows = cursor.fetchall()
conn.close()

# Create DataFrame
df = pd.DataFrame(rows, columns=["timestamp", "close", "sma_5"])
df["timestamp"] = pd.to_datetime(df["timestamp"])

st.write("🔍 Row count:", len(df))
st.dataframe(df)

# Line chart
st.line_chart(df.set_index("timestamp")[["close", "sma_5"]])
