import logging
import logging.config
import json
from pythonjsonlogger import jsonlogger

with open("../loginfo.json") as f:
    config = json.load(f)
    logging.config.dictConfig(config)

logger = logging.getLogger()
logger.debug("Test debug message.")

test = {"Time": 0.5,
        "x": 15,
        "y": 22}

logger.info(json.dumps(test))



