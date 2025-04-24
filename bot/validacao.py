def analisar_entrada_com_pesos(df, estrategias_selecionadas, pesos, risco):
    sinais = {'COMPRA': 0, 'VENDA': 0, 'NEUTRO': 0}

    for nome, resultado in estrategias_selecionadas.items():
        peso = pesos.get(nome, 1)
        sinais[resultado] += peso

    tipo = max(sinais, key=sinais.get)
    if sinais[tipo] < 2 or tipo == "NEUTRO":
        return None  # não há consenso suficiente para entrada

    ultimo_candle = df.iloc[-1]
    preco = ultimo_candle['close']

    if tipo == "COMPRA":
        stop = preco * 0.98
        alvo = preco + (preco - stop) * risco
    elif tipo == "VENDA":
        stop = preco * 1.02
        alvo = preco - (stop - preco) * risco
    else:
        return None

    return {
        'tipo': tipo,
        'entrada': round(preco, 2),
        'stop': round(stop, 2),
        'alvo': round(alvo, 2)
    }
