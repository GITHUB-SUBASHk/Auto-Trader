import asyncio, json
import websockets
from market_feed_base import MarketFeedBase

class MarketFeedZerodha(MarketFeedBase):
    def __init__(self, symbols, tick_callback, api_key, access_token):
        self.symbols = symbols
        self.tick_callback = tick_callback
        self.api_key = api_key
        self.access_token = access_token
        self.ws_url = "wss://ws.kite.zerodha.com/quote"  # Zerodha WebSocket URL

    async def connect(self):
        async with websockets.connect(self.ws_url) as ws:
            # authenticate
            auth_msg = json.dumps({
                "a": self.api_key,
                "v": 3,
                "client_id": self.access_token
            })
            await ws.send(auth_msg)

            # subscribe
            sub_msg = json.dumps({"t": "subscribe", "i": self.symbols})
            await ws.send(sub_msg)
            
            print("Connected to Zerodha WebSocket...")

            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                # example: {'tradable': True, 'ltp': 1825, 'instrument_token': 12345}
                for token, tick in data.items():
                    ltp = tick.get("ltp", 0)
                    await self.tick_callback(token, ltp)

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.connect())
