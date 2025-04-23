from dotenv import load_dotenv
import os
import pandas as pd
from binance.client import Client
from bot.indicadores import calcular_rsi, calcular_smas
from bot.estrategias import usar_rsi, usar_sma

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")

client = Client(api_key, api_secret)

klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR, limit=40)

df = pd.DataFrame(klines, coluns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
    'close_time', 'quote_asset_volume', 'number_of_trades',
    'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'])

df['close'] = df['close'].astype(float)

# Aplica os indicadores
df = calcular_rsi(df)
df = calcular_smas(df)
df = calcular_macd(df)
df = calcular_bollinger(df)
df = calcular_estocastico(df)

# Aplica as estrategias

rsi_signal = usar_rsi(df)
sma_signal = usar_sma(df)

print("📊 Resultados das Estratégias:")
print(f"RSI:        {usar_rsi(df)}")
print(f"SMA:        {usar_sma(df)}")
print(f"MACD:       {usar_macd(df)}")
print(f"Bollinger:  {usar_bollinger(df)}")
print(f"Estocástico:{usar_estocastico(df)}")
