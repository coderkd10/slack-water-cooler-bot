import logging
import yaml
import sys
from os import path

def createLogger(name, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'):
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler()
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter(format)
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def loadConfig(filename="config.yml"):
    try:
        config_path = path.join( path.dirname(__file__), filename )
        with open(config_path, "rb") as f:
            config = yaml.safe_load(f)
    except FileNotFoundError:
        print("Could not read the configuration file - {}. Make sure it exits and is readable.".format(config_path))
        sys.exit(1)
    return config
