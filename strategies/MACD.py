import math
import backtrader as bt

class MACDStrategy(bt.Strategy):
    params = (('fast', 12), ('slow', 26), ('signal', 9), ('order_percentage', 0.95), ('ticker', 'USD'))

    def __init__(self):
        self.macd = bt.indicators.MACDHisto(self.data.close, period_me1=self.params.fast, period_me2=self.params.slow, period_signal=self.params.signal)

    def next(self):
        if self.position.size == 0:
            if self.macd.histo[0] > 0 and self.macd.histo[-1] <= 0:
                amount_to_invest = (self.params.order_percentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close[0])
                print("Comprar {} acciones de {} a {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.macd.histo[0] < 0 and self.macd.histo[-1] >= 0:
                print("Vender {} acciones de {} a {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()
