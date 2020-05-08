import sys
import time
import requests
import numpy as np

from progress.bar import Bar


class Seventh:
    def __init__(self, path):
        self.path = path  # Base client path
        self.conn = requests.Session()

        self.set_state(self.connect())
        self.initial = (self.account, self.holding)

    def connect(self):
        try:
            assert self.conn.get(self.path + "/").text == "LIVE", "Connection refused"
            print("Connection succeeded")
            return self.conn.get(self.path + "/data").json()

        except:
            print("Connection failed")
            exit()

    def set_state(self, state):
        self.historical = np.array(state["historical"])
        self.buyprice, self.sellprice = state["buy"], state["sell"]
        self.account, self.holding = state["account"], state["holding"]

    def sell(self, amount=None):  # Amount in BTC
        if amount is None:
            amount = self.holding
        self.set_state(
            self.conn.post(self.path + "/trade/sell", data={"amount": amount}).json()
        )

    def buy(self, amount=None):  # Amount in USD
        if amount is None:
            amount = abs(self.holding * self.buyprice)
        self.set_state(
            self.conn.post(self.path + "/trade/buy", data={"amount": amount}).json()
        )

    def hold(self):
        self.set_state(
            self.conn.post(self.path + "/trade/hold", data={"amount": 0}).json()
        )

    def resolve_strategy(self):
        if self.holding > 0:
            return self.sell()

        if self.holding < 0:
            return self.buy()

    def strategy(self):
        return self.hold()

    def run(self, days):
        for _ in Bar("Running", fill="=", suffix="%(eta)d sec left").iter(range(days)):
            self.strategy()
            time.sleep(0.5)

        # Purge account holdings
        if self.holding > 0:
            self.sell()
        elif self.holding < 0:
            self.buy(self.holding * self.buyprice)

    def eval(self):
        results = f"""
        ----- Backtrading Results -----
        Initial Account: {self.initial[0]}
        Final Account: {self.account}
        Final Holdings: {self.holding}
        Profit: {self.account - self.initial[0]}
        Yield: {100 * (self.account - self.initial[0])/self.initial[0]:.2f}%
        """
        return results
