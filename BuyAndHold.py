import backtrader as bt

class BuyAndHold(bt.Strategy):
    params = (('order_percentage', 1.0), ('ticker', 'BTC'))

    def _init_(self):
        pass

    def next(self):
        if self.position.size == 0:
            amount_to_invest = self.params.order_percentage * self.broker.cash
            self.size = amount_to_invest / self.data.close[0]
            self.buy(size=self.size)