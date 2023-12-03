import math
import backtrader as bt

class NuestraStrategy(bt.Strategy):
    # gc es para golden cross
    params = (
        ('gc_fast', 50), ('gc_slow', 200), ('gc_order_percentage', 0.95),
        ('macd_fast', 12), ('macd_slow', 26), ('macd_signal', 9), ('macd_order_percentage', 0.95),
        ('rsi_period', 14), ('rsi_overbought', 70), ('rsi_oversold', 30),
        ('rsi_order_percentage', 0.95),
        ('ticker', 'USD')
    )

    def __init__(self):
        # Golden Cross corto plazo
        self.gc_fast_ma = bt.indicators.SMA(self.data.close, period=self.params.gc_fast)
        # Golden Cross largo plazo
        self.gc_slow_ma = bt.indicators.SMA(self.data.close, period=self.params.gc_slow)
        self.gc_crossover = bt.indicators.CrossOver(self.gc_fast_ma, self.gc_slow_ma)

        # MACD
        self.macd = bt.indicators.MACDHisto(
            self.data.close, period_me1=self.params.macd_fast, period_me2=self.params.macd_slow, period_signal=self.params.macd_signal
        )

        # RSI
        self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)

    # c_buy es por custom_buy, un metodo que hacemos nosotros
    def c_buy(self, indicator):
        amount_to_invest = (self.params.gc_order_percentage * self.broker.cash)
        size = math.floor(amount_to_invest / self.data.close[0])
        print(indicator + ": Buy {} shares of {} at {}".format(size, self.params.ticker, self.data.close[0]))
        self.buy(size=size)
    
    def c_sell(self, indicator):
        print(indicator + ": Sell {} shares of {} at {}".format(self.position.size, self.params.ticker, self.data.close[0]))
        self.close()

    def next(self):
        # Estrategia agresiva para la compra: consideramos comprar si cualquier indicador lo indica.
        if self.position.size == 0:
            # Consideramos comprar
            ## Golden Cross condition
            if self.gc_crossover > 0 :
                self.c_buy("Golden Cross")

            ## MACD condition
            elif self.macd.histo[0] > 0 and self.macd.histo[-1] <= 0:
                self.c_buy("MACD")

            ## RSI condition
            elif self.rsi < self.params.rsi_oversold:
                self.c_buy("RSI")

        elif self.position.size > 0:
            # Estrategia agresiva para la compra: consideramos comprar si cualquier indicador lo indica.
            # Consideramos comprar nuevamente
            ## Golden Cross condition
            if self.gc_crossover > 0 :
                self.c_buy("Golden Cross")

            ## MACD condition
            elif self.macd.histo[0] > 0 and self.macd.histo[-1] <= 0:
                self.c_buy("MACD")

            # Estrategia conservadora para la venta: consideramos vender si cualquier indicador lo indica.
            # Consideramos vender
            ## Golden Cross exit condition
            if self.gc_crossover < 0:
                self.c_sell("Golden Cross")

            ## MACD exit condition
            elif self.macd.histo[0] < 0 and self.macd.histo[-1] >= 0:
                self.c_sell("MACD")

            ## RSI exit condition
            elif self.rsi > self.params.rsi_overbought:
                self.c_sell("RSI")
