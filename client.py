#!/usr/bin/env python

import requests
import numpy as np


class Seventh:
    def __init__(self, path):
        self.path = path  # Base client path
        self.conn = requests.Session()

        self.set_state(self.connect())

    def connect(self):
        assert self.conn.get(self.path + "/").text == "LIVE", "Connection refused"
        return self.conn.get(self.path + "/data").json()

    def set_state(self, state):
        self.historical = np.array(state["historical"])
        self.buyprice, self.sellprice = state["buy"], state["sell"]
        self.account, self.holding = state["account"], state["holding"]

    def sell(self, amount=1):  # Amount in BTC
        self.set_state(
            self.conn.post(self.path + "/trade/sell", data={"amount": amount}).json()
        )

    def buy(self, amount=1):  # Amount in USD
        self.set_state(
            self.conn.post(self.path + "/trade/buy", data={"amount": amount}).json()
        )

    def hold(self):
        self.set_state(
            self.conn.post(self.path + "/trade/hold", data={"amount": 0}).json()
        )

    def run(self):
        pass


if __name__ == "__main__":
    client = Seventh("http://localhost:8000")
    print(client.account, client.holding)
    client.buy(100)
    print(client.account, client.holding)
    client.sell(client.holding)
    print(client.account, client.holding)
