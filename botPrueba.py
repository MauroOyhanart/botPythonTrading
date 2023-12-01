from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
from strategies.GoldenCross import GoldenCross
from strategies.DeathCross import DeathCross
from strategies.MACD import MACDStrategy
from strategies.BuyAndHold import BuyAndHold
import backtrader as bt 
from PIL import Image

if __name__ == '__main__':
    cerebro = bt.Cerebro()

    dataDAY = bt.feeds.YahooFinanceCSVData(
        dataname='./dataset/orcl-1995-2014.txt',
        fromdate=datetime.datetime(1995, 11, 1),
        todate=datetime.datetime(2014, 11, 29),
        reverse=False
    )

    cerebro.adddata(dataDAY)
    cerebro.addstrategy(MACDStrategy)
    cerebro.broker.set_cash(10000.0)
    saldoInicial = cerebro.broker.getvalue()
    print('Saldo Inicial: %.2f' % saldoInicial)

    cerebro.run()
    cerebro.plot()
    saldoFinal = cerebro.broker.getvalue()
    print('Saldo Final: %.2f' % saldoFinal)
    saldoFinal = (saldoFinal * 100 / saldoInicial) - 100
    print('Porcentaje de ganancias: %.2f' % saldoFinal)
