import logging
import json
import sys

def createLogger(name, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def loadConfig(filename="config.json"):
    try:
        with open(filename, "rb") as f:
            j = json.load(f)
    except FileNotFoundError:
        print("Could not read the configuration file - {}. Make sure it exits in the current directory and is readable.".format(filename))
        sys.exit(1)
    return j
