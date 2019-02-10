import requests
import xml.etree.ElementTree as xml
from backend import constants, logger

enabled = False
plex_pass = False
notification = False
state = False
host = ""

def getVersion():
    try:
        request = requests.get(host+constants.PLEX_IDENTITY)
        if(request.status_code is 200):
            return xml.fromstring(request.content).attrib['version']
        else:
            raise Exception()
    except:
        return False
