import requests
import json
import time
from kafka import KafkaProducer

# Initialize the Kafka Producer
# 'localhost:9092' is the address we set in docker-compose
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

def get_crypto_price():
    # Fetching live BTC price from Binance (No API key needed)
    url = "https://api.binance.com/api/v3/ticker/price?symbol=BTCUSDT"
    try:
        response = requests.get(url)
        data = response.json()
        return data
    except Exception as e:
        print(f"Error fetching data: {e}")
        return None

print("🚀 Starting Producer... Press Ctrl+C to stop.")

while True:
    price_data = get_crypto_price()
    
    if price_data:
        print(f"📡 Sending to Kafka: {price_data}")
        # 'stock-prices' is the name of our Kafka topic
        producer.send('stock-prices', price_data)
        
    # Wait 5 seconds before fetching the next price
    time.sleep(5)