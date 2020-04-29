#!/usr/bin/env python

import requests
import numpy as np


class Seventh:
    def __init__(self, path):
        self.path = path  # Base client path
        self.conn = requests.Session()

        self.state = self.connect()

    def connect(self):
        assert self.conn.get(self.path + "/").text == "LIVE", "Connection refused"
        return self.conn.get(self.path + "/data")

    def run(self):
        pass


if __name__ == "__main__":
    client = Seventh("http://localhost:8000")
