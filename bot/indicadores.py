import ta
import pandas as pd

def calcular_rsi(df, periodo=14):
    df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=periodo).rsi()
    return df

def calcular_smas(df, curta=9, longa=21):
    df['sma_curta'] = ta.trend.SMAIndicator(close=df['close'], window=curta).sma_indicator()
    df['sma_longa'] = ta.trend.SMAIndicator(close=df['close'], window=longa).sma_indicator()
    return df

def calcular_macd(df):
    macd = ta.trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

def calcular_bollinger(df, janela=20):
    bb = ta.volatility.BollingerBands(close=df['close'], window=janela)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    return df

def calcular_estocastico(df):
    stoch = ta.momentum.StochasticOscillator(high=df['high'], low=df['low'], close=df['close'])
    df['stoch_k'] = stoch.stoch()
    df['stoch_d'] = stoch.stoch_signal()
    return df