from AlethieumAevoSDK import AevoClient
from clientConfig import clientConfig
from loguru import logger as log

aevo = AevoClient(**clientConfig)


transaction = aevo.rest_get_apikey()
log.info(f"API Key: {transaction}")