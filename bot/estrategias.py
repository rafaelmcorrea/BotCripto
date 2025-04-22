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