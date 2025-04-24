# analise_individual.py

from bot.indicadores import calcular_rsi, calcular_smas, calcular_macd, calcular_bollinger, calcular_estocastico
from bot.estrategias import usar_rsi, usar_sma, usar_macd, usar_bollinger, usar_estocastico
from bot.validacao import analisar_entrada_com_pesos
import pandas as pd

estrategias_disponiveis = {
    'RSI': usar_rsi,
    'SMA': usar_sma,
    'MACD': usar_macd,
    'BOLLINGER': usar_bollinger,
    'ESTOCASTICO': usar_estocastico
}

def analisar_par(df, variaveis, pesos_indicadores, risco):
    df = calcular_rsi(df)
    df = calcular_smas(df)
    df = calcular_macd(df)
    df = calcular_bollinger(df)
    df = calcular_estocastico(df)

    estrategias_usadas = {}
    contagem = {'COMPRA': 0, 'VENDA': 0, 'NEUTRO': 0}

    for nome, func in estrategias_disponiveis.items():
        if variaveis[nome].get():
            resultado = func(df)
            estrategias_usadas[nome] = resultado
            contagem[resultado] += 1

    entrada = analisar_entrada_com_pesos(df, estrategias_usadas, pesos_indicadores, risco)

    return estrategias_usadas, contagem, entrada
