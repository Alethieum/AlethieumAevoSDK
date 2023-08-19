from AlethieumAevoSDK import AevoClient

client = AevoClient(
    signing_key="0xaa9ab4166a39c50764b3229e089473f183a3565d068d3f6bcf3cb109dd4ad70f",
    wallet_address="0x13B7e774A1685210Ef13dF32eC9D0AAF4E3e6014",
    api_key="67rhYQeypNRqYPek3gjXvZKcVMrKARZ5",
    api_secret="06c65e235d5f1d53ff94723721d7c2ed9f64bbc8f0bbbcb0dceb4cd2ad1dba82",
    env="mainnet",
)
# markets = client.get_orderbook("ETH-PERP")
# print(markets) # This should work if your client is setup right

# async def main():
#     aevo = AevoClient(
#         signing_key="0xaa9ab4166a39c50764b3229e089473f183a3565d068d3f6bcf3cb109dd4ad70f",
#         wallet_address="0x13B7e774A1685210Ef13dF32eC9D0AAF4E3e6014",
#         api_key="67rhYQeypNRqYPek3gjXvZKcVMrKARZ5",
#         api_secret="06c65e235d5f1d53ff94723721d7c2ed9f64bbc8f0bbbcb0dceb4cd2ad1dba82",
#         env="mainnet",
#     )

#     await aevo.open_connection()

#     # We pass in the instrument ID as the first parameter
#     # ONLY RUN THIS LINE IN TESTNET
#     await aevo.create_order(1, True, 10, 100)

# asyncio.run(main())

import numpy as np

def get_midmarket_price(client, market):
    orderbook = client.get_orderbook(market)
    best_bid = float(orderbook['bids'][0][0])
    best_ask = float(orderbook['asks'][0][0])
    midmarket_price = np.mean([best_bid, best_ask])
    return round(midmarket_price, 2)


midmarket_price = get_midmarket_price(client, "ETH-PERP")
print(midmarket_price)