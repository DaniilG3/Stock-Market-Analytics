from kafka import KafkaProducer
import yfinance as yf
import json
import time

# Set up Kafka producer
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# Stock symbols
stocks = ["AAPL", "TSLA", "AMZN", "MSFT", "GOOG"]

while True:
    for symbol in stocks:
        stock = yf.Ticker(symbol)
        hist = stock.history(period="1d", interval="1m")

        if hist.empty:
            print(f"⚠️ {symbol}: no data returned, skipping.")
            continue

        latest = hist.tail(1)
        data = {
            "symbol": symbol,
            "timestamp": str(latest.index[0]),
            "close": float(latest['Close'].values[0]),
            "volume": int(latest['Volume'].values[0])
        }

        # Send to Kafka
        producer.send('stock-stream', value=data)
        print(f"✅ Sent to Kafka: {data}")
    
    time.sleep(60)  # Run every minute
