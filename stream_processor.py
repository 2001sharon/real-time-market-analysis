# Initialize state before the loop
last_signal = "HOLD"

for message in consumer:
    data = message.value
    curr_price = float(data['price'])
    
    if prev_price is not None:
        price_window.append(curr_price - prev_price)
    
    prev_price = curr_price

    if len(price_window) == 14:
        # 1. Calculate RSI
        gains = [x for x in price_window if x > 0]
        losses = [abs(x) for x in price_window if x < 0]
        avg_gain = sum(gains) / 14
        avg_loss = sum(losses) / 14
        
        if avg_loss == 0:
            rsi = 100
        else:
            rs = avg_gain / avg_loss
            rsi = 100 - (100 / (1 + rs))
        
        # 2. Determine Current Recommendation
        current_recommendation = "HOLD 😐"
        short_signal = "HOLD" # Simple version for tracking
        
        if rsi < 30:
            current_recommendation = "JOIN (BUY) 🚀 - Market is Oversold"
            short_signal = "JOIN"
        elif rsi > 70:
            current_recommendation = "EXIT (SELL) ⚠️ - Market is Overbought"
            short_signal = "EXIT"
            
        # 3. ONLY print/send if the signal has changed
        # This prevents the "Trade Log" from filling up with 100 HOLDs
        if short_signal != last_signal:
            analysis_result = {
                "symbol": data['symbol'],
                "price": curr_price,
                "rsi": round(rsi, 2),
                "signal": current_recommendation,
                "short_signal": short_signal  # For easy filtering in the dashboard
            }
            
            print(f"🚨 SIGNAL CHANGE: {current_recommendation} (RSI: {round(rsi, 2)})")
            producer.send('stock-analysis', analysis_result)
            last_signal = short_signal