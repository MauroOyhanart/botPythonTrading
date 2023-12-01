import math
import backtrader as bt

# Estrategia: Cross Method -> Golden Cross.
# Dos SMA, una a corto plazo, otra a largo plazo. La de 50 cruza a la de 200 hacia arriba, indicando un posible cambio a tendencia alcista.

class GoldenCross(bt.Strategy):
    params = (('fast', 50), ('slow', 200), ('order_porcentage', 0.95), ('ticker', 'USD'))

    def __init__(self):
        self.fast_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.fast, plotname='Media Móvil - 50 Periodos'
        )

        self.slow_moving_average = bt.indicators.SMA(
            self.data.close, period=self.params.slow, plotname='Media Móvil - 200 Periodos'
        )

        self.crossover = bt.indicators.CrossOver(self.fast_moving_average, self.slow_moving_average)

    def next(self):
        if self.position.size == 0:
            if self.crossover > 0:
                amount_to_invest = (self.params.order_porcentage * self.broker.cash)
                self.size = math.floor(amount_to_invest / self.data.close)
                print("Comprar {} acciones de {} a {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.buy(size=self.size)

        if self.position.size > 0:
            if self.crossover < 0:
                print("Vender {} acciones de {} a {}".format(self.size, self.params.ticker, self.data.close[0]))
                self.close()
