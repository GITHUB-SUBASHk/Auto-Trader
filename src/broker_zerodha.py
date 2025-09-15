import os
from kiteconnect import KiteConnect
from broker_base import BrokerBase

class ZerodhaBroker(BrokerBase):
    def __init__(self, api_key, api_secret, token_file="/app/data/access_token.txt"):
        self.api_key = api_key
        self.api_secret = api_secret
        self.token_file = token_file

        if not os.path.exists(token_file):
            raise Exception("Access token not found. Run token_gen.py first")

        with open(token_file,"r") as f:
            self.access_token = f.read().strip()

        self.kite = KiteConnect(api_key=self.api_key)
        self.kite.set_access_token(self.access_token)

    def authenticate(self):
        return True

    def place_order(self, symbol, qty, transaction_type, stop_loss=None):
        try:
            order = self.kite.place_order(
                variety="regular",
                exchange="NSE",
                tradingsymbol=symbol,
                transaction_type=transaction_type,
                quantity=qty,
                product="CNC",
                order_type="MARKET"
            )
            return f"Zerodha Order placed: {order}"
        except Exception as e:
            return f"Zerodha Order failed: {str(e)}"

    def get_positions(self):
        return self.kite.positions()
