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


class Random(Seventh):
    def strategy(self):
        delta = self.historical[1:] - self.historical[:-1]

        if self.holding != 0:
            return self.resolve_strategy()

        if delta[-10:].mean() > 0:
            return self.buy()

        return self.sell(0.02)


class SizedMAV(Seventh):
    def strategy(self, size=0.4):
        delta = self.historical[1:] - self.historical[:-1]

        if self.holding != 0:
            return self.resolve_strategy()

        if delta[-10:].mean() > 0:
            return self.buy(self.account * size)

        return self.sell(size)


class Stochastic(Seventh):
    def strategy(self, size=0.4):
        delta = self.historical[1:] - self.historical[:-1]

        if self.holding != 0:
            return self.resolve_strategy()

        if not (delta[-10:].mean() > 0 or np.random.uniform() > 0.7):
            return self.buy(self.account * size)

        return self.sell(size)
