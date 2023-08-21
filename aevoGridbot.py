# # Description: Imports needed

from clientConfig import clientConfig
from AlethieumAevoSDK import AevoClient
import asyncio
import json
from pprint import pprint
import pendulum
import time
import numpy as np
from loguru import logger
 
### CLIENT ###
# # Description: Please add your API key and secret to the clientConfig file.
# # Description: After importing the clientConfig, we can now create the client object.
# # Description: Please ensure that the clientConfig is correct before running the script.

client = AevoClient(**clientConfig)

### TASKS ###
# # Description: This section is for tasks

def get_midmarket_price(client, market):
    orderbook = client.get_orderbook(market)
    best_bid = float(orderbook["bids"][0][0])
    best_ask = float(orderbook["asks"][0][0])
    midmarket_price = np.mean([best_bid, best_ask])
    return round(midmarket_price, 2)
    # # Function: This task gets the midmarket price of the instrument.


### GRIDBOT CONFIG ###
# # Description: This file contains the tasks that will be executed by the celery worker

instrument_id = 1
instrument_name = "ETH-PERP"
orderSize = 0.01
gridSize = 1
girdLines = 10

### DATA ###
# # Description: This section is for data needed for the script

midmarket_price = get_midmarket_price(client, instrument_name)


### GRIDBOT ###
# # Description: This file contains the tasks that will be executed by the celery worker


async def aevo_gridbot():
    try:
        await client.open_connection()
        await client.subscribe_fills()

        async for msg in client.read_messages():
            message = json.loads(msg)
            if "data" in message and "success" in message["data"]:
                if message["data"]["success"] == True:
                    logger.info(
                        "🔌 Websocket connected at "
                        + str(pendulum.now())
                        + " to account "
                        + message["data"]["account"]
                    )
                    logger.info("🧑‍🍳 Starting Gridbot...")
                    for i in range(0, girdLines):
                        await client.create_order(
                            instrument_id,
                            True,
                            midmarket_price - (i * gridSize),
                            orderSize,
                        )
                        await asyncio.sleep(1)  # add a 1 second delay
                        await client.create_order(
                            instrument_id,
                            False,
                            midmarket_price + (i * gridSize),
                            orderSize,
                        )
                        await asyncio.sleep(1)  # add a 1 second delay
                else:
                    logger.info(message)
            elif "data" in message and "fill" in message["data"]:
                if message["data"]["fill"]["side"] == "buy":
                    logger.info("buy order filled")
                    logger.info("creating sell order")
                    await client.create_order(
                        instrument_id,
                        False,
                        float(message["data"]["fill"]["price"]) + gridSize,
                        orderSize,
                    )
                    logger.info(
                        "created new sell order at "
                        + str(float(message["data"]["fill"]["price"]) + gridSize)
                    )
                elif message["data"]["fill"]["side"] == "sell":
                    logger.info("sell order filled")
                    logger.info("creating buy order")
                    await client.create_order(
                        instrument_id,
                        True,
                        float(message["data"]["fill"]["price"]) - gridSize,
                        orderSize,
                    )
                    logger.info(
                        "created new buy order at "
                        + str(float(message["data"]["fill"]["price"]) - gridSize)
                    )
            else:
                logger.info(message)
    except Exception as e:
        logger.error(f"Connection closed unexpectedly: {e}")
        logger.info("Cancelling all orders...")
        await client.cancel_all_orders(instrument_id)
        logger.info("All orders cancelled.")
        logger.info("Websocket disconnected at " + str(pendulum.now()))
        logger.info("")
        logger.info("Attempting to reconnect at " + str(pendulum.now()) + "...")
        logger.info("")
        time.sleep(1)
        await aevo_gridbot()


def start_gridbot():
    asyncio.get_event_loop().run_until_complete(aevo_gridbot())


start_gridbot()
