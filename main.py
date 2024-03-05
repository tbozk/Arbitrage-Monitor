import asyncio
import websockets
import json
from datetime import datetime, timedelta

pair_data = {}
triplets = []
pair_to_triplet_indices = {}
last_print_time = {}


def read_triplets_file(filename):
    with open(filename, 'r') as f:
        for line in f:
            triplet = line.strip()[1:-1].split(', ')
            triplet = [pair.strip("'") for pair in triplet]
            triplets.append(triplet)
    return triplets


def on_message(message):
    global pair_to_triplet_indices, pair_data

    message_data = json.loads(message)

    symbol = message_data["data"]["s"]  # This is the "s" value, representing the symbol (e.g., BTCUSDT)
    bid_price = message_data["data"]["b"]  # This is the "b" value, representing the best bid price
    ask_price = message_data["data"]["a"]  # This is the "a" value, representing the best ask price

    # check if the pair exists
    if symbol not in pair_data:
        pair_data[symbol] = {"ask": -1, "bid": -1}

    # Update this pair's data
    pair_data[symbol]["bid"] = float(bid_price)
    pair_data[symbol]["ask"] = float(ask_price)

    # print(f"Symbol: {symbol}, Bid Price: {bid_price}, Ask Price: {ask_price}")
    for triplet_index in pair_to_triplet_indices[symbol]:
        triplet = triplets[triplet_index]
        A, B, C = triplet
        triplet_str = f"{A}-{B}-{C}"

        if all(pair in pair_data for pair in [A, B, C]) and all(
                pair_data[pair]["bid"] != -1 and pair_data[pair]["ask"] != -1 for pair in [A, B, C]):
            print_threshold = timedelta(seconds=5)

            # Check if we've printed this arbitrage recently
            now = datetime.now()
            if triplet_str not in last_print_time or (now - last_print_time[triplet_str]) > print_threshold:
                # Checking for arbitrage opportunity and printing...
                last_print_time[triplet_str] = now
            # Checking for arbitrage opportunity
                if pair_data[A]["ask"] * pair_data[B]["ask"] < pair_data[C]["ask"]:
                    print("Arbitrage detected: {}, {}, {}".format(A, B, C))
                    print(
                        f"ASK Prices: {A}: {pair_data[A]['ask']}, {B}: {pair_data[B]['ask']},  {C}: {pair_data[C]['ask']}")
                    print()
                if pair_data[A]["bid"] * pair_data[B]["bid"] > pair_data[C]["bid"]:
                    print("Arbitrage detected: {}, {}, {}".format(A, B, C))
                    print(
                        f"BID Prices of {A}: {pair_data[A]['bid']}, {B}: {pair_data[B]['bid']}, {C}: {pair_data[C]['bid']}")
                    print()


async def consumer_handler(websocket):
    async for message in websocket:
        on_message(message)


async def connect_and_consume(uri):
    async with websockets.connect(uri) as websocket:
        await consumer_handler(websocket)
    print("Connection secured.")


async def main():
    TRIPLET_NO = 150 #pick the first 150 triplets from all triplets.
    #this ensures that the number of pairs does not exceed 500 since 150 * 3 = 450

    global triplets, pair_to_triplet_indices

    filename = 'ALL_TRIPLETS.txt'
    triplets = read_triplets_file(filename)  # MAKE THIS ACCESSIBLE FROM ALL FUNCTIONS
    pair_to_triplet_indices = {}  # MAKE THIS ACCESSIBLE FROM ALL FUNCTIONS

    for index, triplet in enumerate(triplets[:TRIPLET_NO]):
        for pair in triplet:
            if pair not in pair_to_triplet_indices:
                pair_to_triplet_indices[pair] = {index}
            else:
                pair_to_triplet_indices[pair].add(index)

    # print(pair_to_triplet_indices)

    base_endpoint = "wss://stream.binance.com:9443"
    last_endpoint = "/stream?streams="
    for triplet in triplets[:TRIPLET_NO]:
        for pair in triplet:
            last_endpoint += f"{pair.lower()}@bookTicker/"

    stream_endpoint = base_endpoint + last_endpoint[:-1]
    #print(stream_endpoint)

    await connect_and_consume(stream_endpoint)


if __name__ == "__main__":
    asyncio.run(main())


