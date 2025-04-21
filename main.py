from binance.client import Client
from dotenv import load_dotenv
import os

#carrega as variaveis do .env
load_dotenv()
api_key = os.getenv("BINANCE_API_KEY")
api_secret = os.getenv("BINANCE-API_SECRET")

#Inicializa o cliente na Binance
client = Client(api_key, api_secret)

#Obtém os últimos 5 candles de 1 hora
candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR, limit=5)

import pandas as pd

#Converte candles em DataFrame
df = pd.DataFrame(candles, coluns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'])

#converte tipos
df['timestamp'] = pd.to.datetime(df['timestamp'], unit='ms')
df['open'] = df['open'].astype(float)
df['high'] = df['high'].astype(float)
df['low'] = df['low'].astype(float)
df['close'] = df['close'].astype(float)
df['volume'] = df['volume'].astype(float)

#Define o índice como timestamp
df.set_index('timestamp', inplice=True)

#Mostra o DataFrame

pint(df[['open', 'high', 'low', 'close', 'volume']])

#mostra abertura e fechamento
for candle in candles:
    print(f"Abertura: {candle[1]} | Fechamento: {candle[4]}")

import ta

#calcula RSI
df['rsi'] = ta.momentum.RSIIndicator(close=df['close'], window=14).rsi()

# Define sinais simples com base no RSI
def verificar_sinal(rsi):
    if rsi < 30:
        return '🔵 Comprar'
    elif rsi > 70:
        return '🔴 Vender'
    else:
        return '🟡 Aguardar'
    
df['sinal'] = df['rsi'].apply(lambda x: verificar_sinal(x) if pd.notna(x) else 'carregando...')

#mostra as últimas linhas com o RSI e o sinal
print(df[['close', 'rsi', 'sinal']].tail())
