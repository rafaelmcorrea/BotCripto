# main.py
import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import os
from binance.client import Client
from bot.scanner import escanear_mercado

load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
client = Client(api_key, api_secret)

janela = tk.Tk()
janela.title("Bot de Cripto")
janela.geometry("500x650")

# Par e intervalo
tk.Label(janela, text="Par (ex: BTCUSDT)").pack()
entrada_simbolo = tk.Entry(janela)
entrada_simbolo.insert(0, "BTCUSDT")
entrada_simbolo.pack(pady=5)

tk.Label(janela, text="Intervalo").pack()
combo_intervalo = ttk.Combobox(janela, values=["1m", "5m", "15m", "1h", "4h", "1d"])
combo_intervalo.set("1h")
combo_intervalo.pack(pady=5)

tk.Label(janela, text="Risco (ex: 1.5 para RR 1:1.5)").pack()
entrada_risco = tk.Entry(janela)
entrada_risco.insert(0, "2")
entrada_risco.pack(pady=5)

tk.Label(janela, text="Consenso mínimo").pack()
entrada_consenso = tk.Entry(janela)
entrada_consenso.insert(0, "3")
entrada_consenso.pack(pady=5)

# Estratégias
tk.Label(janela, text="Estratégias:").pack()
from bot.estrategias import usar_rsi, usar_sma, usar_macd, usar_bollinger, usar_estocastico
variaveis = {}
estrategias_disponiveis = ['RSI', 'SMA', 'MACD', 'BOLLINGER', 'ESTOCASTICO']
for nome in estrategias_disponiveis:
    var = tk.BooleanVar(value=True)
    chk = tk.Checkbutton(janela, text=nome, variable=var)
    chk.pack(anchor='w')
    variaveis[nome] = var

# Resultado
resultado_text = tk.Text(janela, height=20, wrap=tk.WORD)
resultado_text.pack(fill='both', expand=True)

# Botão buscar
btn_buscar = tk.Button(janela, text="Buscar Sinal", bg='green', fg='white', 
    command=lambda: escanear_mercado(client, combo_intervalo, entrada_risco, entrada_consenso, resultado_text, variaveis))
btn_buscar.pack(pady=10)

janela.mainloop()
