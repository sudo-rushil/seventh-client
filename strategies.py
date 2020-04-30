import numpy as np
from seventh_client import Seventh


class Trial(Seventh):
    def strategy(self):
        if self.holding == 0:
            return self.buy()

        return self.sell(self.holding)


# class MAV(Seventh):
#     def strategy(self):
#         print(self.historical.dtype)
#         return self.hold()
