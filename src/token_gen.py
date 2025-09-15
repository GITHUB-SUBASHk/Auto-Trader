import os
from kiteconnect import KiteConnect
from upstox_api.api import Upstox
from dotenv import load_dotenv

load_dotenv()

BROKER = os.getenv("BROKER")
API_KEY = os.getenv("API_KEY")
API_SECRET = os.getenv("API_SECRET")

if BROKER == "ZERODHA":
    kite = KiteConnect(api_key=API_KEY)
    print("Zerodha login URL:", kite.login_url())
    request_token = input("Enter request token from URL: ")
    data = kite.generate_session(request_token, api_secret=API_SECRET)
    with open("/app/data/access_token.txt", "w") as f:
        f.write(data["access_token"])
    print("Zerodha access token saved")

elif BROKER == "UPSTOX":
    print("For Upstox, go to their auth page to generate token")
    access_token = input("Paste Upstox access token: ")
    with open("/app/data/access_token.txt", "w") as f:
        f.write(access_token)
    print("Upstox access token saved")
