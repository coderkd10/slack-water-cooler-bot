import requests
from bs4 import BeautifulSoup

TOPIC_GENERATOR_URL = "https://www.conversationstarters.com/random.php"

def generateTopic():
    r = requests.get(TOPIC_GENERATOR_URL)
    soup = BeautifulSoup(r.text, "html.parser")
    return soup.text
