def usar_rsi(df):
    ultimo_rsi = df['rsi'].iloc[-1]
    if ultimo_rsi < 30:
        return 'COMPRA'
    elif ultimo_rsi > 70:
        return 'VENDA'
    else:
        return 'NEUTRO'

def usar_sma(df):
    if df['sma_curta'].iloc[-1] > df['sma_longa'].iloc[-1]:
        return 'COMPRA'
    elif df['sma_curta'].iloc[-1] < df['sma_longa'].iloc[-1]:
        return 'VENDA'
    else:
        return 'NEUTRO'

def usar_macd(df):
    if df['macd'].iloc[-1] > df['macd_signal'].iloc[-1]:
        return 'COMPRA'
    elif df['macd'].iloc[-1] < df['macd_signal'].iloc[-1]:
        return 'VENDA'
    else:
        return 'NEUTRO'

def usar_bollinger(df):
    close = df['close'].iloc[-1]
    upper = df['bb_upper'].iloc[-1]
    lower = df['bb_lower'].iloc[-1]
    if close < lower:
        return 'COMPRA'
    elif close > upper:
        return 'VENDA'
    else:
        return 'NEUTRO'

def usar_estocastico(df):
    k = df['stoch_k'].iloc[-1]
    d = df['stoch_d'].iloc[-1]
    if k < 20 and k > d:
        return 'COMPRA'
    elif k > 80 and k < d:
        return 'VENDA'
    else:
        return 'NEUTRO'