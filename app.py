import tkinter as tk
from tkinter import ttk
from dotenv import load_dotenv
import os
import pandas as pd
from binance.client import Client

from bot.indicadores import calcular_rsi, calcular_smas, calcular_macd, calcular_bollinger, calcular_estocastico
from bot.estrategias import usar_rsi, usar_sma, usar_macd, usar_bollinger, usar_estocastico
from bot.validacao import analisar_entrada_com_pesos

# Configura API
load_dotenv()
api_key = os.getenv("API_KEY")
api_secret = os.getenv("API_SECRET")
client = Client(api_key, api_secret)

# Estratégias disponíveis
estrategias_disponiveis = {
    'RSI': usar_rsi,
    'SMA': usar_sma,
    'MACD': usar_macd,
    'BOLLINGER': usar_bollinger,
    'ESTOCASTICO': usar_estocastico
}

# Pesos de cada estratégia
pesos_indicadores = {
    'RSI': 1.0,
    'SMA': 1.2,
    'MACD': 1.5,
    'BOLLINGER': 1.3,
    'ESTOCASTICO': 1.0
}

moedas_para_escanear = ["BTCUSDT", "ETHUSDT", "BNBUSDT", "SOLUSDT", "XRPUSDT", "ADAUSDT", "DOGEUSDT"]

def buscar_dados():
    try:
        simbolo = entrada_simbolo.get().upper()
        intervalo = combo_intervalo.get()
        risco = float(entrada_risco.get())

        klines = client.get_klines(symbol=simbolo, interval=intervalo, limit=100)
        df = pd.DataFrame(klines, columns=[
            'timestamp', 'open', 'high', 'low', 'close', 'volume',
            'close_time', 'quote_asset_volume', 'number_of_trades',
            'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
        ])
        df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)

        df = calcular_rsi(df)
        df = calcular_smas(df)
        df = calcular_macd(df)
        df = calcular_bollinger(df)
        df = calcular_estocastico(df)

        resultado_text.delete('1.0', tk.END)
        resultado_text.insert(tk.END, "📊 Resultados das Estratégias Selecionadas:\n\n")

        resumo = {'COMPRA': 0, 'VENDA': 0, 'NEUTRO': 0}
        estrategias_usadas = {}

        for nome, func in estrategias_disponiveis.items():
            if variaveis[nome].get():
                res = func(df)
                estrategias_usadas[nome] = res
                resumo[res] += 1
                resultado_text.insert(tk.END, f"{nome}: {res}\n")

        resultado_text.insert(tk.END, f"\n📈 RESUMO:\nCOMPRA: {resumo['COMPRA']} | VENDA: {resumo['VENDA']} | NEUTRO: {resumo['NEUTRO']}\n")

        entrada = analisar_entrada_com_pesos(df, estrategias_usadas, pesos_indicadores, risco)
        if isinstance(entrada, dict) and entrada.get('entrada'):
            resultado_text.insert(tk.END, f"\n🚀 POSSÍVEL ENTRADA DE {entrada['tipo']} DETECTADA:\n")
            resultado_text.insert(tk.END, f"ENTRADA: {entrada['entrada']}\nSTOP: {entrada['stop']}\nALVO: {entrada['alvo']}\n")
        else:
            resultado_text.insert(tk.END, "\n📉 Sem oportunidade clara de entrada.\n")

    except Exception as e:
        resultado_text.insert(tk.END, f"\n❌ Erro ao buscar dados: {e}\n")

def escanear_mercado():
    try:
        intervalo = combo_intervalo.get()
        risco = float(entrada_risco.get())
        minimo_consenso = int(entrada_consenso.get())

        resultado_text.insert(tk.END, "\n\n🔍 ESCANEANDO MERCADO:\n")
        for simbolo in moedas_para_escanear:
            try:
                klines = client.get_klines(symbol=simbolo, interval=intervalo, limit=100)
                df = pd.DataFrame(klines, columns=[
                    'timestamp', 'open', 'high', 'low', 'close', 'volume',
                    'close_time', 'quote_asset_volume', 'number_of_trades',
                    'taker_buy_base_volume', 'taker_buy_quote_volume', 'ignore'
                ])
                df[['open', 'high', 'low', 'close']] = df[['open', 'high', 'low', 'close']].astype(float)

                df = calcular_rsi(df)
                df = calcular_smas(df)
                df = calcular_macd(df)
                df = calcular_bollinger(df)
                df = calcular_estocastico(df)

                estrategias_usadas = {}
                for nome, func in estrategias_disponiveis.items():
                    if variaveis[nome].get():
                        res = func(df)
                        estrategias_usadas[nome] = res

                contagem = {'COMPRA': 0, 'VENDA': 0, 'NEUTRO': 0}
                for r in estrategias_usadas.values():
                    contagem[r] += 1

                if contagem['COMPRA'] >= minimo_consenso:
                    resultado_text.insert(tk.END, f"{simbolo}: ✅ FORTE CONSENSO DE COMPRA ({contagem['COMPRA']})\n")
                elif contagem['VENDA'] >= minimo_consenso:
                    resultado_text.insert(tk.END, f"{simbolo}: 🔻 FORTE CONSENSO DE VENDA ({contagem['VENDA']})\n")
                else:
                    resultado_text.insert(tk.END, f"{simbolo}: Sem consenso suficiente (Compra: {contagem['COMPRA']}, Venda: {contagem['VENDA']})\n")

            except Exception as e:
                resultado_text.insert(tk.END, f"❌ Erro ao analisar {simbolo}: {e}\n")
    except Exception as e:
        resultado_text.insert(tk.END, f"❌ Erro ao escanear mercado: {e}\n")

# Interface Tkinter
janela = tk.Tk()
janela.title("Bot de Cripto")
janela.geometry("540x720")

# Inputs
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

tk.Label(janela, text="Mínimo de consenso para sinal (ex: 3)").pack()
entrada_consenso = tk.Entry(janela)
entrada_consenso.insert(0, "3")
entrada_consenso.pack(pady=5)

# Estratégias
tk.Label(janela, text="Estratégias:").pack()
variaveis = {}
for nome in estrategias_disponiveis.keys():
    var = tk.BooleanVar(value=True)
    chk = tk.Checkbutton(janela, text=nome, variable=var)
    chk.pack(anchor='w')
    variaveis[nome] = var

# Botões
btn_buscar = tk.Button(janela, text="Buscar Sinal", command=buscar_dados, bg='green', fg='white')
btn_buscar.pack(pady=5)

btn_scan = tk.Button(janela, text="Escanear Mercado", command=escanear_mercado, bg='blue', fg='white')
btn_scan.pack(pady=5)

# Área de resultado
resultado_text = tk.Text(janela, height=20, wrap=tk.WORD)
resultado_text.pack(fill='both', expand=True)

# Iniciar
janela.mainloop()
