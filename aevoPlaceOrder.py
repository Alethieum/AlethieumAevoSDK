from AlethieumAevoSDK import AevoClient
from clientConfig import clientConfig
from loguru import logger as log



# Add Credentials
aevo = AevoClient(**clientConfig)

# Create a market order
order_params = {
    "instrument_id":  # Instrument ID number
    "is_buy":   # True for long order, false for short order
    "quantity":  # Number of contracts. In 6 decimals fixed number
}

order = aevo.rest_create_market_order(**order_params)
log.info(f"Order: {order}")
