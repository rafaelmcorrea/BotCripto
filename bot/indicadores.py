import pandas as pd
import ta

#calcula RSI
def calcular_rsi(df, periodo=14):
    df['rsi'] = ta.momentum.RSIINdicator(close=df['close'],window=periodo).rsi()
    return df

def calcular_smas(df, curta=9, longa=21):
    df['sma_curta'] = ta.trend.SMAIndicator(close=df['close'], windoww=curta).sma_indicator()
    df['sma_longa'] = ta.trend.SMAIndicator(close=df['close'], window=longa).sma_indicator()
    return df
