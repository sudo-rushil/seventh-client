import numpy as np
from seventh_client import Seventh


class Trial(Seventh):
    def strategy(self):
        if self.holding == 0:
            return self.buy()

        return self.sell(self.holding)


class MAV(Seventh):
    def strategy(self):
        ten = self.historical[-10:].mean()
        thirty = self.historical[-30:].mean()

        if self.holding > 0:
            return self.sell()

        if self.holding < 0:
            return self.buy()

        if ten > thirty:
            return self.sell(0.02)

        return self.hold()
