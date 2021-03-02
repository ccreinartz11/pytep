import logging
import logging.config
import json
from pythonjsonlogger import jsonlogger

with open("../loginfo.json") as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger()
logger.debug("Test debug message.")

logger.info("Test")



