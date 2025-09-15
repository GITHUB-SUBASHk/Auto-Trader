import asyncio
import json
import os
import websockets
from market_feed_base import MarketFeedBase
from dotenv import load_dotenv

load_dotenv()

UPSTOX_WS_URL = "wss://ws.upstox.com/live"  # placeholder, use actual URL
API_KEY = os.getenv("API_KEY")
ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")

class MarketFeed:
    def __init__(self, symbols, callback):
        """
        symbols: list of symbols to subscribe
        callback: function to call on each tick
        """
        self.symbols = symbols
        self.callback = callback

    async def connect(self):
        async with websockets.connect(UPSTOX_WS_URL) as ws:
            # authenticate
            auth_msg = json.dumps({"api_key": API_KEY, "access_token": ACCESS_TOKEN})
            await ws.send(auth_msg)

            # subscribe to symbols
            sub_msg = json.dumps({"action": "subscribe", "symbols": self.symbols})
            await ws.send(sub_msg)

            print("Connected to Upstox WebSocket...")
            
            while True:
                msg = await ws.recv()
                data = json.loads(msg)
                # pass tick data to strategy
                await self.callback(data)

    def start(self):
        asyncio.get_event_loop().run_until_complete(self.connect())
