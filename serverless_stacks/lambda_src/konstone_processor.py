# -*- coding: utf-8 -*-
import json
import logging
import os

# Configura logger global (una vez por contenedor Lambda)
LOGGER = logging.getLogger()
if not LOGGER.hasHandlers():
    logging.basicConfig()
LOGGER.setLevel(level=os.getenv('LOG_LEVEL', 'DEBUG').upper())


def lambda_handler(event, context):
    LOGGER.info(f"received_event: {event}")

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": event
        })
    }
