import requests
import sys
import json

import utils
import zoom
import topics as topicGenerator

logger = utils.createLogger(__file__)

config = utils.loadConfig()
if "slack" not in config:
    logger.error("slack key not present in config json")
    sys.exit(1)
slack_conf = config["slack"]
if "webhook_url" not in slack_conf or "channel" not in slack_conf:
    logger.error("webhook_url or channel not present in slack config")
    sys.exit(1)

WEBHOOK_URL = slack_conf["webhook_url"]
CHANNEL = slack_conf["channel"]
BOT_USERNAME = slack_conf.get("username", "water-cooler-bot")
BOT_ICON_EMOJI = slack_conf.get("icon_emoji", ":water-cooler:")

def ping(num_topics=3):
    topics = [topicGenerator.generateTopic() for _ in range(num_topics)]
    meetingUrl = zoom.getMeetingUrl()
    msg = "<!channel> You must be really thirsty, its time to get a glass of water! :glass_of_milk:\n" +\
            "Gather around the water cooler ya folks - {}\n\n".format(meetingUrl) +\
            "While you're at it, here are some topics that you may find interesting to discuss -\n" +\
            "\n".join(["{}. {}".format(i+1, topic) for i, topic in enumerate(topics)])
    payload = {
        "text": msg,
        "channel": CHANNEL,
        "username": BOT_USERNAME,
        "icon_emoji": BOT_ICON_EMOJI
    }
    r = requests.post(WEBHOOK_URL, json=payload)
    if r.status_code != 200:
        logger.error("some error occured while sending slack message. slack API return code - {}".format(r.status_code))
        logger.debug("payload for slack webhook - {}".format(json.dumps(payload)))
