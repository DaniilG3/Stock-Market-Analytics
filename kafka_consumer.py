import json
import psycopg2
from kafka import KafkaConsumer

# Connect to Kafka
consumer = KafkaConsumer(
    'stock-topic',  # <- change to your actual topic
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8'))
)

# Connect to PostgreSQL (RDS)
conn = psycopg2.connect(
    host='stock-data-db.cniggw0umcgr.us-east-2.rds.amazonaws.com',
    database='postgres',
    user='postgres',
    password='jymwex-vogMed-4dedqy',
    sslmode='require'
)
cursor = conn.cursor()

# Start consuming messages
for message in consumer:
    data = message.value  # expected format: {'ticker': ..., 'price': ..., 'volume': ...}
    try:
        cursor.execute("""
            INSERT INTO stock_data (ticker, price, volume)
            VALUES (%s, %s, %s);
        """, (data['ticker'], data['price'], data['volume']))
        conn.commit()
        print(f"Inserted: {data}")
    except Exception as e:
        print("Insert failed:", e)
