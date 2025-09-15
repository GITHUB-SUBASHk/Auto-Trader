async def tick_handler(symbol, ltp):
    # Check for stop-loss / take-profit hit
    pos = broker.get_positions().get(symbol, None)
    if pos and pos["qty"] > 0:
        if pos["side"] == "BUY":
            if ltp <= pos["sl"]:
                print(f"Stop-loss hit for {symbol} at {ltp}")
                broker.place_order(symbol, pos["qty"], "SELL", ltp)
            elif ltp >= pos["tp"]:
                print(f"Target hit for {symbol} at {ltp}")
                broker.place_order(symbol, pos["qty"], "SELL", ltp)
        elif pos["side"] == "SELL":
            if ltp >= pos["sl"]:
                print(f"Stop-loss hit for {symbol} at {ltp}")
                broker.place_order(symbol, pos["qty"], "BUY", ltp)
            elif ltp <= pos["tp"]:
                print(f"Target hit for {symbol} at {ltp}")
                broker.place_order(symbol, pos["qty"], "BUY", ltp)

    # Run strategy
    trade_signal = simple_strategy(symbol, ltp)
    if not trade_signal:
        return

    result = broker.place_order(
        symbol,
        trade_signal["qty"],
        trade_signal["transaction_type"],
        price=ltp,
        sl=trade_signal.get("sl"),
        tp=trade_signal.get("tp")
    )
    print(result)

    # Update unrealized PnL
    pnl_update = broker.update_pnl_on_tick(symbol, ltp)
    if pnl_update:
        print("PnL Update:", pnl_update)
