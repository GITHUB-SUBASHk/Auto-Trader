import csv, os, datetime
import random
from broker_base import BrokerBase

class PaperBroker(BrokerBase):
    def __init__(self, file_path="/app/data/paper_trades.csv"):
        self.file_path = file_path
        if not os.path.exists(self.file_path):
            with open(self.file_path,"w",newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Time","Symbol","Action","Qty","Price","Status","PnL"])
        self.positions = {}  # net positions per symbol
        self.last_buy_price = {}  # to compute PnL

    def authenticate(self):
        return True

    def _get_live_price(self, symbol):
        # Simulate live tick; replace with broker feed for real tick
        return round(random.uniform(1400,1600),2)

    def place_order(self, symbol, qty, action):
        price = self._get_live_price(symbol)
        pnl = 0

        net_qty = self.positions.get(symbol,0)

        if action=="BUY":
            self.positions[symbol] = net_qty + qty
            self.last_buy_price[symbol] = price

        elif action=="SELL":
            if net_qty>0:
                pnl = (price - self.last_buy_price.get(symbol, price)) * qty
                self.positions[symbol] = net_qty - qty
            else:
                self.positions[symbol] = net_qty - qty

        # Log trade
        with open(self.file_path,"a",newline="") as f:
            writer = csv.writer(f)
            writer.writerow([
                datetime.datetime.now().strftime("%H:%M:%S"),
                symbol,
                action,
                qty,
                price,
                "Executed",
                round(pnl,2)
            ])
        return f"{action} {qty} {symbol} @ {price} | PnL={round(pnl,2)}"

    def get_positions(self):
        return self.positions
import csv
import os
from datetime import datetime

class PaperBroker:
    def __init__(self, csv_file="data/trades.csv"):
        self.csv_file = csv_file
        self.positions = {}  # {symbol: {"qty": int, "avg_price": float, "side": "BUY/SELL"}}
        self.realized_pnl = 0.0

        # Ensure data dir exists
        os.makedirs(os.path.dirname(self.csv_file), exist_ok=True)

        # Init CSV
        if not os.path.exists(self.csv_file):
            with open(self.csv_file, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerow(["Time", "Symbol", "Action", "Qty", "Price", "Status", "PnL"])

    def place_order(self, symbol, qty, action, price, sl=None, tp=None):
        now = datetime.now().strftime("%H:%M:%S")
        pnl = 0
        status = "Executed"

        # If symbol not in positions, initialize
        if symbol not in self.positions:
            self.positions[symbol] = {"qty": 0, "avg_price": 0.0, "side": None, "sl": sl, "tp": tp}

        pos = self.positions[symbol]

        if action == "BUY":
            # If no existing position → open
            if pos["qty"] == 0:
                pos["qty"] = qty
                pos["avg_price"] = price
                pos["side"] = "BUY"
                pos["sl"], pos["tp"] = sl, tp
            else:
                # Add to existing BUY
                if pos["side"] == "BUY":
                    total_cost = pos["avg_price"] * pos["qty"] + price * qty
                    pos["qty"] += qty
                    pos["avg_price"] = total_cost / pos["qty"]
                # If SELL position exists → close partially/fully
                elif pos["side"] == "SELL":
                    diff = min(qty, pos["qty"])
                    pnl = (pos["avg_price"] - price) * diff  # because short
                    self.realized_pnl += pnl
                    pos["qty"] -= diff
                    if pos["qty"] == 0:
                        pos["side"], pos["avg_price"] = None, 0.0

        elif action == "SELL":
            if pos["qty"] == 0:
                pos["qty"] = qty
                pos["avg_price"] = price
                pos["side"] = "SELL"
                pos["sl"], pos["tp"] = sl, tp
            else:
                if pos["side"] == "SELL":
                    total_cost = pos["avg_price"] * pos["qty"] + price * qty
                    pos["qty"] += qty
                    pos["avg_price"] = total_cost / pos["qty"]
                elif pos["side"] == "BUY":
                    diff = min(qty, pos["qty"])
                    pnl = (price - pos["avg_price"]) * diff
                    self.realized_pnl += pnl
                    pos["qty"] -= diff
                    if pos["qty"] == 0:
                        pos["side"], pos["avg_price"] = None, 0.0

        # Log to CSV
        with open(self.csv_file, "a", newline="") as f:
            writer = csv.writer(f)
            writer.writerow([now, symbol, action, qty, price, status, pnl])

        return {
            "symbol": symbol,
            "action": action,
            "qty": qty,
            "price": price,
            "pnl": pnl,
            "realized_pnl": self.realized_pnl,
            "positions": self.positions[symbol]
        }

    def update_pnl_on_tick(self, symbol, ltp):
        """Update unrealized PnL on each tick"""
        if symbol not in self.positions or self.positions[symbol]["qty"] == 0:
            return None

        pos = self.positions[symbol]
        if pos["side"] == "BUY":
            unrealized = (ltp - pos["avg_price"]) * pos["qty"]
        else:  # SELL
            unrealized = (pos["avg_price"] - ltp) * pos["qty"]

        return {
            "symbol": symbol,
            "unrealized_pnl": unrealized,
            "realized_pnl": self.realized_pnl,
            "total_pnl": unrealized + self.realized_pnl
        }

    def get_positions(self):
        return self.positions
