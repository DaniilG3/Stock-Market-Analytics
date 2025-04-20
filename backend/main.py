from fastapi import FastAPI
from pydantic import BaseModel
import google.generativeai as genai
from fastapi.middleware.cors import CORSMiddleware
import os
import psycopg2
from urllib.parse import urlparse

# 👇 Replace with your actual Gemini API key
genai.configure(api_key="AIzaSyANJbLAzRLq_UVocYf2Q63tq9uLgfv01S4")

for m in genai.list_models():
    print("✅ Available model:", m.name)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Input model for stock data
class StockInput(BaseModel):
    symbol: str
    sma: float
    rsi: float
    percent_change: float
    trend: str

# Gemini-powered summary generator
def generate_stock_summary(symbol, sma, rsi, percent_change, trend):
    prompt = (
        f"Given the following indicators for {symbol}:\n"
        f"- SMA-5: {sma}\n"
        f"- RSI: {rsi}\n"
        f"- Percent change today: {percent_change}%\n"
        f"- Current trend: {trend}\n\n"
        "Write a short summary and recommend a short-term and long-term action."
    )
    model = genai.GenerativeModel(model_name="gemini-1.5-pro")
    response = model.generate_content(prompt)
    return response.text.strip()

# Test root endpoint
@app.get("/")
def root():
    return {"message": "🚀 Gemini stock insight API is running!"}

# Main AI summary endpoint
@app.post("/summary")
def get_summary(data: StockInput):
    result = generate_stock_summary(
        symbol=data.symbol,
        sma=data.sma,
        rsi=data.rsi,
        percent_change=data.percent_change,
        trend=data.trend
    )
    return {
        "symbol": data.symbol,
        "summary": result
    }


@app.get("/chart/{symbol}")
def get_chart(symbol: str):
    # Get your full DATABASE URL string from Railway and parse it
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:tkNfhRCaMdTErIMQKdinVfyGVDYugEKK@ballast.proxy.rlwy.net:37791/railway")
    parsed = urlparse(DATABASE_URL)

    # Connect to PostgreSQL
    conn = psycopg2.connect(
        dbname=parsed.path[1:],
        user=parsed.username,
        password=parsed.password,
        host=parsed.hostname,
        port=parsed.port
    )

    cursor = conn.cursor()
    cursor.execute("""
        SELECT DISTINCT ON (DATE_TRUNC('minute', timestamp)) 
            timestamp::time, close, sma_5
        FROM stocks
        WHERE symbol = %s AND sma_5 IS NOT NULL
        ORDER BY DATE_TRUNC('minute', timestamp) DESC
        LIMIT 10
    """, (symbol,))
    
    rows = cursor.fetchall()
    cursor.close()
    conn.close()

    rows.reverse()
    chart_data = [
        {"timestamp": row[0].strftime("%H:%M"), "close": float(row[1]), "sma_5": float(row[2])}
        for row in rows
    ]
    return chart_data
