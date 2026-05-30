from kafka import KafkaConsumer, KafkaProducer
import json
import time

consumer = KafkaConsumer(
    'stock-prices',
    bootstrap_servers='localhost:9092',
    auto_offset_reset='latest',
    value_deserializer=lambda x: json.loads(x.decode('utf-8'))
)

producer = KafkaProducer(
    bootstrap_servers='localhost:9092',
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
)

prices = []

print("🧠 Analysis Engine Started... Waiting for data from Producer...")

for message in consumer:
    data = message.value
    price = float(data['price'])

    prices.append(price)

    if len(prices) > 20:
        prices.pop(0)

    sma = sum(prices) / len(prices)

    # Trend
    if price > sma:
        trend = "UPTREND 📈"
        signal = "BUY"
    elif price < sma:
        trend = "DOWNTREND 📉"
        signal = "SELL"
    else:
        trend = "SIDEWAYS ➖"
        signal = "HOLD"

    processed_data = {
        "symbol": data["symbol"],
        "price": price,
        "sma": round(sma, 2),
        "trend": trend,
        "signal": signal
    }

    print("📊 Processed:", processed_data)

    producer.send("stock-analysis", processed_data)
    producer.flush()