import tkinter as tk
from tkinter import ttk
from bot.estrategias import usar_rsi, usar_sma, usar_macd, usar_bollinger, usar_estocastico
from bot.indicadores import calcular_rsi, calcular_smas, calcular_macd, calcular_bollinger, calcular_estocastico
from binance.client import Client
from dotenv import load_dotenv
import os
import pandas as pd

# Carrega as variáveis de ambiente
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
client = Client(api_key, api_secret)

# Função que executa as estratégias
def rodar_bot():
    klines = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR, limit=40)

    df = pd.DataFrame(klines, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume',
        'close_time', 'quote_asset_volume', 'number_of_trades',
        'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'])

    df['close'] = df['close'].astype(float)
    df['high'] = df['high'].astype(float)
    df['low'] = df['low'].astype(float)

    df = calcular_rsi(df)
    df = calcular_smas(df)
    df = calcular_macd(df)
    df = calcular_bollinger(df)
    df = calcular_estocastico(df)

    resultados = {
        'RSI': usar_rsi(df),
        'SMA': usar_sma(df),
        'MACD': usar_macd(df),
        'Bollinger': usar_bollinger(df),
        'Estocástico': usar_estocastico(df)
    }

    output_text.delete(1.0, tk.END)  # Limpa
    for nome, resultado in resultados.items():
        output_text.insert(tk.END, f"{nome}: {resultado}\n")

# Interface
root = tk.Tk()
root.title("Bot Cripto - Estratégias")

frame = ttk.Frame(root, padding=20)
frame.grid()

ttk.Label(frame, text="Bot de Estratégias Cripto", font=("Helvetica", 16)).grid(column=0, row=0, columnspan=2, pady=10)

ttk.Button(frame, text="Executar Estratégias", command=rodar_bot).grid(column=0, row=1, pady=10)

output_text = tk.Text(frame, width=50, height=10)
output_text.grid(column=0, row=2, columnspan=2, pady=10)

root.mainloop()