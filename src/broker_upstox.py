import os
from upstox_api.api import Upstox
from broker_base import BrokerBase

class UpstoxBroker(BrokerBase):
    def __init__(self, api_key, api_secret, access_token=None):
        self.api_key = api_key
        self.api_secret = api_secret
        self.access_token = access_token or os.getenv("ACCESS_TOKEN")

        if not self.access_token:
            raise Exception("Access token required for Upstox. Generate via token_gen.py")

        self.client = Upstox(self.api_key, self.access_token)

    def authenticate(self):
        return True

    def place_order(self, symbol, qty, transaction_type, stop_loss=None):
        try:
            order = self.client.place_order(
                transaction_type=transaction_type,
                instrument=self.client.get_instrument_by_symbol("NSE_EQ", symbol),
                quantity=qty,
                order_type="MARKET",
                product="D",
                duration="DAY"
            )
            return f"Upstox Order placed: {order}"
        except Exception as e:
            return f"Upstox Order failed: {str(e)}"

    def get_positions(self):
        return self.client.get_positions()
