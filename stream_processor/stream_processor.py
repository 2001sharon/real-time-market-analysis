from kafka import KafkaConsumer, KafkaProducer
import json
from collections import deque

# 1. Setup Consumer to read raw prices from the producer
consumer = KafkaConsumer(
    'stock-prices',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest'
)

# 2. Setup Producer to send analyzed results to a new topic
producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

# We use the last 10 prices to calculate a moving average
price_window = deque(maxlen=10)

print("🧠 Analysis Engine Started... Waiting for data from Producer...")

for message in consumer:
    data = message.value
    current_price = float(data['price'])
    symbol = data['symbol']
    
    price_window.append(current_price)
    
    # We need 10 data points before we can calculate a trend
    if len(price_window) == 10:
        avg_price = sum(price_window) / len(price_window)
        trend = "UP 📈" if current_price > avg_price else "DOWN 📉"
        
        analysis_result = {
            "symbol": symbol,
            "current_price": current_price,
            "average_price": round(avg_price, 2),
            "trend": trend
        }
        
        print(f"✅ Analyzed: {symbol} | Price: {current_price} | Trend: {trend}")
        
        # Send this analysis to a NEW Kafka topic
        producer.send('stock-analysis', analysis_result)