import json


with open('TICKER_DATA', 'r') as f:
    data = f.read()

# Parse JSON
tickers = json.loads(data)


symbols = [ticker['symbol'] for ticker in tickers]


with open('PAIRS_EXTRACTED', 'w') as f:
    f.write(str(symbols))