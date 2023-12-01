from __future__ import (absolute_import, division, print_function, unicode_literals)
import datetime
from strategies.GoldenCross import GoldenCross
from strategies.DeathCross import DeathCross
from strategies.MACD import MACDStrategy
from strategies.BuyAndHold import BuyAndHold
import backtrader as bt 
from PIL import Image

if __name__ == '__main__':
    # Inicialización del objeto cerebro
    cerebro = bt.Cerebro()

    # Configuración de los datos históricos (en este caso, datos de Yahoo Finance)
    dataDAY = bt.feeds.YahooFinanceCSVData(
        dataname='./dataset/orcl-1995-2014.txt',
        fromdate=datetime.datetime(1995, 11, 1),
        todate=datetime.datetime(2014, 11, 29),
        reverse=False
    )

    # Adicion de los datos al cerebro
    cerebro.adddata(dataDAY)

    # Adicion de la estrategia MACD al cerebro
    cerebro.addstrategy(MACDStrategy)

    # Configuracion del capital inicial
    cerebro.broker.set_cash(10000.0)
    
    # Configuración de la comisión (0.001%)
    cerebro.broker.setcommission(commission=0.00001)

    # Impresion del saldo inicial
    saldoInicial = cerebro.broker.getvalue()
    print('Saldo Inicial: %.2f' % saldoInicial)

    # Ejecucion del backtest
    cerebro.run()

    # Generacion y muestra del grafico
    cerebro.plot()

    # Calculo y muestra del saldo final
    saldoFinal = cerebro.broker.getvalue()
    print('Saldo Final: %.2f' % saldoFinal)

    # Calculo y muestra del porcentaje de ganancias
    saldoFinal = (saldoFinal * 100 / saldoInicial) - 100
    print('Porcentaje de ganancias: %.2f' % saldoFinal)
