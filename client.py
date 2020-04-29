#!/usr/bin/env python

import sys
import requests
from time import sleep
import numpy as np


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

    def sell(self, amount=0.01):  # Amount in BTC
        self.set_state(
            self.conn.post(self.path + "/trade/sell", data={"amount": amount}).json()
        )

    def buy(self, amount=100):  # Amount in USD
        self.set_state(
            self.conn.post(self.path + "/trade/buy", data={"amount": amount}).json()
        )

    def hold(self):
        self.set_state(
            self.conn.post(self.path + "/trade/hold", data={"amount": 0}).json()
        )

    def strategy(self):
        if self.holding == 0:
            return self.buy()

        return self.sell(self.holding)

    def run(self, days):
        for _ in range(days):
            self.strategy()
            sleep(2)

    def eval(self):
        results = f"""
        ----- Backtrading Results -----
        Initial Account: {self.initial[0]}
        Final Account: {self.account}
        Profit: {self.account - self.initial[0]}
        Yield: {(self.account - self.initial[0])/self.initial[0]:.2f}%
        """
        return results


if __name__ == "__main__":
    flatten = lambda l: [item for sublist in l for item in sublist]
    args = flatten(map(lambda s: s.split(":"), sys.argv))
    assert len(args) == 3, "No server name given"

    client = Seventh(f"http://{args[1]}:{args[2]}")
    client.run(10)
    print(client.eval())
