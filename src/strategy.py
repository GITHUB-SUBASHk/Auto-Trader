def simple_strategy(symbol, ltp):
    # Demo strategy: Buy if price is even, Sell if odd
    if int(ltp) % 2 == 0:
        return {"symbol": symbol, "qty": 50, "transaction_type": "BUY", "sl": ltp - 10, "tp": ltp + 20}
    else:
        return {"symbol": symbol, "qty": 50, "transaction_type": "SELL", "sl": ltp + 10, "tp": ltp - 20}
