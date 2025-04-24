import pandas as pd
from bot.indicadores import calcular_rsi, calcular_smas, calcular_macd, calcular_bollinger, calcular_estocastico
from bot.estrategias import usar_rsi, usar_sma, usar_macd, usar_bollinger, usar_estocastico
from bot.validacao import analisar_entrada_com_pesos

estrategias_disponiveis = {
    'RSI': usar_rsi,
    'SMA': usar_sma,
    'MACD': usar_macd,
    'BOLLINGER': usar_bollinger,
    'ESTOCASTICO': usar_estocastico
}

def escanear_mercado(client, moedas, intervalo, risco, minimo_consenso, variaveis, pesos_indicadores, resultado_text):
    resultado_text.insert('end', "\n\n🔍 ESCANEANDO MERCADO:\n")
    for simbolo in moedas:
        try:
            resultado_text.insert('end', f"\nAnalisando {simbolo}...\n")
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
                    resultado = func(df)
                    estrategias_usadas[nome] = resultado

            contagem = {'COMPRA': 0, 'VENDA': 0, 'NEUTRO': 0}
            for r in estrategias_usadas.values():
                contagem[r] += 1

            if contagem['COMPRA'] >= minimo_consenso:
                resultado_text.insert('end', f"{simbolo}: ✅ FORTE CONSENSO DE COMPRA ({contagem['COMPRA']})\n")
            elif contagem['VENDA'] >= minimo_consenso:
                resultado_text.insert('end', f"{simbolo}: 🔻 FORTE CONSENSO DE VENDA ({contagem['VENDA']})\n")
            else:
                resultado_text.insert('end', f"{simbolo}: Sem consenso suficiente (Compra: {contagem['COMPRA']}, Venda: {contagem['VENDA']})\n")

            entrada = analisar_entrada_com_pesos(df, estrategias_usadas, pesos_indicadores, risco)
            resultado_text.insert('end', f"[DEBUG] Estratégias: {estrategias_usadas}\n")
            resultado_text.insert('end', f"[DEBUG] Entrada detectada: {entrada}\n")

            if isinstance(entrada, dict) and entrada.get('entrada'):
                resultado_text.insert('end', f"\n🚀 POSSÍVEL ENTRADA DE {entrada['tipo']} DETECTADA:\n")
                resultado_text.insert('end', f"ENTRADA: {entrada['entrada']}\nSTOP: {entrada['stop']}\nALVO: {entrada['alvo']}\n")
            else:
                resultado_text.insert('end', "📉 Sem oportunidade clara de entrada.\n")

        except Exception as e:
            resultado_text.insert('end', f"❌ Erro ao analisar {simbolo}: {e}\n")
