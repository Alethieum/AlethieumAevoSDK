import asyncio
from AlethieumAevoSDK import AevoClient

async def main():
    aevo = AevoClient(
        signing_key="0xaa9ab4166a39c50764b3229e089473f183a3565d068d3f6bcf3cb109dd4ad70f",
        wallet_address="0x13B7e774A1685210Ef13dF32eC9D0AAF4E3e6014",
        api_key="67rhYQeypNRqYPek3gjXvZKcVMrKARZ5",
        api_secret="06c65e235d5f1d53ff94723721d7c2ed9f64bbc8f0bbbcb0dceb4cd2ad1dba82",
        env="testnet",
    )

    await aevo.open_connection() # need to do this first to open wss connections
    await aevo.subscribe_ticker("ticker:ETH:PERPETUAL")

    async for msg in aevo.read_messages():
        print(msg)

if __name__ == "__main__":
    asyncio.run(main())