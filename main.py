from binance.client import Client
api_key =''
api_secret = ''

client = Client(api_key, api_secret)

candles = client.get_klines(symbol='BTCUSDT', interval=Client.KLINE_INTERVAL_1HOUR, limit=5)

for candle in candles:
    print(f"Abertura: {candle[1]} | Fechamento: {candle[4]}")