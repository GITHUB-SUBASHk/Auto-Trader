def validate_trade(trade):
    if trade["qty"] <= 0:
        return False, "Invalid quantity"
    if not trade["symbol"]:
        return False, "Invalid symbol"
    return True, "OK"
