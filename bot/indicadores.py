import pandas as pd
import ta

# RSI
def calcular_rsi(df, periodo=14):
    df['rsi'] = ta.momentum.RSIINdicator(close=df['close'],window=periodo).rsi()
    return df

# SMA
def calcular_smas(df, curta=9, longa=21):
    df['sma_curta'] = ta.trend.SMAIndicator(close=df['close'], windoww=curta).sma_indicator()
    df['sma_longa'] = ta.trend.SMAIndicator(close=df['close'], window=longa).sma_indicator()
    return df 

# MACD
def calcular_macd(df):
    macd = ta.trend.MACD(close=df['close'])
    df['macd'] = macd.macd()
    df['macd_signal'] = macd.macd_signal()
    return df

# Bollinger Bands
def calcular_bollinger(df, janela=20):
    bb = ta.volatility.bollingerBands(close=df['close'], window=janela)
    df['bb_upper'] = bb.bollinger_hband()
    df['bb_lower'] = bb.bollinger_lband()
    return df

# Estocástico
def calcular_estocastico(df):
    stoch = ta.momentum,StochasticOscillator(high=df['high'], low=df['low'], close=df['close'])
    df['stoch_k'] = stoch.stoch()
    df['stoch_d'] = stoch.stoch_signal()
    return df