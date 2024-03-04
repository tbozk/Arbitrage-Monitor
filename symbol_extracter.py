import json

# Read data from file
with open('TICKER_DATA', 'r') as f:
    data = f.read()

# Parse JSON data
tickers = json.loads(data)

# Extract symbols
symbols = [ticker['symbol'] for ticker in tickers]

# Write symbols to a file
with open('PAIRS_EXTRACTED', 'w') as f:
    f.write(str(symbols))