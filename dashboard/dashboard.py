import streamlit as st
from kafka import KafkaConsumer
import json
import pandas as pd
import time

# Page Configuration
st.set_page_config(page_title="Live Market Analysis", layout="wide")
st.title("📈 Real-Time Market Trend Dashboard")
st.subheader("Listening to Kafka Topic: `stock-analysis`")

# Initialize the Kafka Consumer
# Note: We read from 'stock-analysis', NOT 'stock-prices'
consumer = KafkaConsumer(
    'stock-analysis',
    bootstrap_servers='localhost:9092',
    value_deserializer=lambda m: json.loads(m.decode('utf-8')),
    auto_offset_reset='latest'
)

# Create placeholders for live updates
col1, col2, col3 = st.columns(3)
price_metric = col1.empty()
avg_metric = col2.empty()
trend_metric = col3.empty()

chart_data = st.empty()
data_history = []

print("🖥️ Dashboard UI is active. Waiting for Kafka messages...")

# Loop through Kafka messages
for message in consumer:
    data = message.value
    
    # Update Metrics
    price_metric.metric("Current Price", f"${data['current_price']}")
    avg_metric.metric("Moving Average", f"${data['average_price']}")
    trend_metric.info(f"Trend: {data['trend']}")
    
    # Update Chart
    data_history.append({
        "Price": data['current_price'],
        "Average": data['average_price']
    })
    
    # Keep only the last 50 points for the chart
    df = pd.DataFrame(data_history[-50:])
    chart_data.line_chart(df)
    
    # Small sleep to keep the UI smooth
    time.sleep(0.1)