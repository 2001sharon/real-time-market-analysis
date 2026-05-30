for message in consumer:
    data = message.value
    
    # Update new metrics
    price_metric.metric("Price", f"${data['price']}")
    trend_metric.info(f"Signal: {data['signal']}")
    
    # Add a specific gauge or text for RSI
    st.write(f"**Current RSI:** {data['rsi']}")
    
    # Pro Tip: Color the background based on RSI
    if data['rsi'] < 30:
        st.success("🔥 BUY OPPORTUNITY")
    elif data['rsi'] > 70:
        st.error("📉 SELL ALERT")
data_history.append({
    "Price": data['price'],
    "RSI": data['rsi'],
    "Overbought (70)": 70,  # This creates the top line
    "Oversold (30)": 30     # This creates the bottom line
})

df = pd.DataFrame(data_history[-50:])

# We'll create two separate charts for better clarity
# 1. Price Chart (Top)
st.subheader("Price vs Moving Average")
st.line_chart(df[["Price"]], use_container_width=True)

# 2. RSI Chart (Bottom)
st.subheader("RSI Momentum Indicator")
st.line_chart(df[["RSI", "Overbought (70)", "Oversold (30)"]], 
              color=["#FF4B4B", "#000000", "#000000"], # RSI in red, limits in black
              use_container_width=True)