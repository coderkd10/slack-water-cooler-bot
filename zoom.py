from base64 import b64encode
import re
import json
import hmac
import hashlib
import requests
import time
import utils
import sys

logger = utils.createLogger(__file__)

ZOOM_USERS_API_URL = "https://api.zoom.us/v2/users/"
ZOOM_CREATE_MEETING_API_URL = "https://api.zoom.us/v2/users/{userId}/meetings"

config = utils.loadConfig()
if "zoom" not in config:
    logger.error("zoom key not found in the config json")
    sys.exit(1)
zoom_conf = config["zoom"]
if "api_key" not in zoom_conf:
    logger.error("api_key not found in zoom config")
    sys.exit(1)
ZOOM_API_KEY = zoom_conf["api_key"]
if "api_secret" not in zoom_conf:
    logger.error("api_secret not found in zoom config")
    sys.exit(1)
ZOOM_API_SECRET = zoom_conf["api_secret"]

def encode(text):
    if isinstance(text, str):
        text = text.encode()
    b64str = b64encode(text).decode()
    return re.sub(r"=+$", "", b64str)

def getZoomAccessToken():
    header = { "alg": "HS256", "typ": "JWT" }
    encodedHeader = encode(json.dumps(header))
    payload = {
        "iss": ZOOM_API_KEY,
        "exp": int(time.time() + 5*60)
    }
    encodedPayload = encode(json.dumps(payload))
    toSign = encodedHeader + "." + encodedPayload
    signatureHmac = hmac.new(ZOOM_API_SECRET.encode(), msg=toSign.encode(), digestmod=hashlib.sha256)
    signature = encode(signatureHmac.digest())
    return toSign + "." + signature

def getZoomUserId():
    headers = {
        "Authorization": "Bearer {}".format(getZoomAccessToken())
    }
    r = requests.get(ZOOM_USERS_API_URL, headers=headers)
    if r.status_code != 200:
        logger.error("zoom users API failed with code {}".format(r.status_code))
        raise ValueError("zoom users API failed", r)
    j = r.json()
    users = j["users"]
    if len(users) == 0:
        logger.error("zoom users API returned without any users")
        raise ValueError("zoom users API returned without any users", r)
    user = users[0]
    userId = user["id"]
    return userId

def getMeetingUrl():
    userId = getZoomUserId()
    payload = {
        "topic": "chilling at the water cooler!",
        # keeping type: scheduled meeting
        # if we use instant meeting then people can't join without the host
        "type": 2,
        "ageda": "just some random water cooler conversations!",
        "settings": {
            "participant_video": True,
            "join_before_host": True,
            "mute_upon_entry": False
        }
    }
    headers = {
        "Authorization": "Bearer {}".format(getZoomAccessToken())
    }
    r = requests.post(ZOOM_CREATE_MEETING_API_URL.format(userId=userId), headers=headers, json=payload)
    j = r.json()
    join_url = "{}?pwd={}".format(j["join_url"], j["encrypted_password"])
    return join_url
