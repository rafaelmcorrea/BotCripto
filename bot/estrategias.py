def usar_rsi(df):
    ultima = df.iloc[-1]
    if ultima['rsi'] < 30:
        return 'COMPRA'
    elif ultima['rsi'] > 70:
        return 'VENDA'
    return 'NEUTRO'

def usar_sma(df):
    ultima = df.iloc[-1]
    if ultima['sma_curta'] > ultima['sma_longa']:
        return 'COMPRA'
    elif ultima['sma_curta'] < ultima['sma_longa']:
        return 'VENDA'
    return 'NEUTRO'

def usar_macd(df):
    ultima = df.iloc[-1]
    if ultima['macd'] > ultima['macd_signal']:
        return 'COMPRA'
    elif ultima['macd'] < ultima['macd_signal']:
        return 'VENDA'
    return 'NEUTRO'

def usar_bollinger(df):
    ultima = df.iloc[-1]
    if ultima['close'] < ultima['bb_lower']:
        return 'COMPRA'
    elif ultima['close'] > ultima['bb_upper']:
        return 'VENDA'
    return 'NEUTRO'

def usar_bollinger(df):
    ultima = df.iloc[-1]
    if ultima['stoch_k'] < 20 and ultima['stoch_d'] < 20:
        return 'COMPRA'
    elif ultima['stoch_k'] > 80 and ultima['stoch_d'] > 80:
        return 'VENDA'
    return 'NEUTRO'