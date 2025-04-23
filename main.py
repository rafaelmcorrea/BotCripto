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

from bot.estrategias import usar_rsi, usar_sma, usar_macd, usar_bollinger, usar_estocastico

# Dicionario de Estratégias
estrategias_disponiveis = {
    'RSI': usar_rsi,
    'SMA': usar_sma,
    'MACD': usar_macd,
    'BOLLINGER': usar_bollinger,
    'ESTOCASTICO': usar_estocastico 
}

print ("\n=== MENU DE ESTRATÉGIAS ===")
for i, nome in enumerate(estrategias_disponiveis.keys(), 1):
    print(f"{i}. {nome}")

opcoes = input("\nDigite os números das estratégias separadas por vírgula (ex: 1,3,5): ")
escolhidas = [int(num.strip()) for num in opcoes.split(',')]

resultados = {'COMPRA': 0, 'VENDA': 0, 'NEUTRO': 0}

print("\n📊 Resultados das Estratégias Escolhidas:")
for i in escolhidas:
    nome = list(estrategias_disponiveis.key())[i - 1]
    funcao = estrategias_disponiveis[nome]
    resultado = funcao(df)
    resultados[resultado] += 1
    print(f"{nome}: {resultado}")

print("\n📈 RESUMO:")
print(f"COMPRA: {resultados['COMPRA']} | VENDA: {resultados['VENDA']} | NEUTRO: {resultados['NEUTRO']}")

