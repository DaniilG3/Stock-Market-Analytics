from kafka import KafkaProducer
import yfinance as yf
import json
import time

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

TICKERS = ['AAPL', 'GOOGL', 'MSFT', 'TSLA']

while True:
    for ticker in TICKERS:
        stock = yf.Ticker(ticker)
        data = stock.info

        message = {
            'ticker': ticker,
            'price': round(data.get('regularMarketPrice', 0), 2),
            'volume': data.get('volume', 0)
        }

        print(f"Sending: {message}")
        producer.send('stock-topic', message)

    time.sleep(10)  # every 10 seconds
