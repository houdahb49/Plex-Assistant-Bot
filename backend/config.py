import configparser
import sys

from colored import stylize
from backend import constants, logger
from backend.api import telegram, sonarr, radarr, ombi, plex

parser = None

def initialize():
    initParser()
    parseConfig()

# Initialize the configuration parser
def initParser():
    global parser
    try:
        parser = configparser.ConfigParser()
        parser.read(constants.CONFIG_FILE)
        if not(len(parser) > 1):
            raise Exception()
        logger.info(__name__, "Configparser initialized")
    except:
        logger.error(__name__, "Failed to load config.ini: Please ensure that a valid config file is located at {}".format(constants.CONFIG_FILE))
        exit()

# Wrapper to parse all configuration data
def parseConfig():
    parseGeneral()
    parseTelegram()
    parseOmbi()
    parsePlex()
    parseRadarr()
    parseSonarr()
    parseAdmins()
    parseNotifications()

def parseGeneral():
    try:
        if('GENERAL' in parser):
            constants.BOT_NAME = parser['GENERAL']['NAME']
            logger.info(__name__, "Parsed general information")
        else:
            raise Exception()
    except:
        logger.error(__name__, "Failed to get general config information: Check your config.ini")
        exit()

def parseNotifications():
    try:
        if('NOTIFICATIONS' in parser):
            constants.NOTIFICATION_TIME = parser['NOTIFICATIONS']['TIME']
            constants.NOTIFICATION_DAY = parser['NOTIFICATIONS']['DAY']
            logger.warning(__name__, "Notification times set: {} @ {}".format(constants.NOTIFICATION_DAY, constants.NOTIFICATION_TIME))
        else:
            raise Exception()
    except:
        logger.error(__name__, "Failed to get notification times: Check your config.ini")
        exit()

# Admin list parsing
def parseAdmins():
    try:
        if('TELEGRAM' in parser):
            for admin in parser['TELEGRAM']['AUTO_ADMINS'].split(','):
                telegram.addAdmin(int(admin.strip()))
                logger.warning(__name__, "Telegram admins: {}".format(telegram.admins))
        else:
            raise Exception()
    except:
        logger.error(__name__, "Failed to get the admin user list: Check your config.ini")
        exit()

# Sonarr API parsing
def parseSonarr():
    if('SONARR' in parser):
        if(parser.getboolean('SONARR', 'ENABLED')):
            sonarr.enabled = True
            sonarr.api = parser['SONARR']['API']
            sonarr.host = parser['SONARR']['HOST']
            sonarr.update_frequency = int(parser['SONARR']['UPDATE_FREQ'])
            sonarr.initialize()
            logger.info(__name__, "Sonarr API parsed")
    else:
        logger.error(__name__, "Could not read the Sonarr configuration values: Check your config.ini")
        exit()

# Radarr API parsing
def parseRadarr():
    if('RADARR' in parser):
        if(parser.getboolean('RADARR', 'ENABLED')):
            radarr.enabled = True
            radarr.api = parser['RADARR']['API']
            radarr.host = parser['RADARR']['HOST']
            radarr.update_frequency = int(parser['RADARR']['UPDATE_FREQ'])
            radarr.initialize()
            logger.info(__name__, "Radarr API parsed")
    else:
        logger.error(__name__, "Could not read the Radarr configuration values: Check your config.ini")
        exit()

# Ombi API parsing
def parseOmbi():
    if('OMBI' in parser):
        if(parser.getboolean('OMBI', 'ENABLED')):
            ombi.enabled = True
            ombi.api = parser['OMBI']['API']
            ombi.host = parser['OMBI']['HOST']
            ombi.initialize()
            logger.info(__name__, "Ombi API parsed")
    else:
        logger.error(__name__, "Failed to initialize Ombi's API: Check your config.ini")
        exit()
    
def parsePlex():
    if('PLEX' in parser):
        if(parser.getboolean('PLEX', 'ENABLED')):
            plex.enabled = True
            plex.host = parser['PLEX']['HOST']
            plex.plex_pass = parser.getboolean('PLEX', 'PLEX_PASS')
            plex.notification = parser.getboolean('PLEX', 'STATUS_NOTIFY')
            version = plex.getVersion()
            if(version):
                logger.info(__name__, "Plex connection established [{}]".format(version))
                plex.state = True
            else:
                logger.error(__name__, "Plex is unreachable, however the bot will continue...")
                plex.state = False
    else:
        logger.error(__name__, "Failed to initialize Plex connection: Check your config.ini")
        exit()

# Telegram API parsing
def parseTelegram():
    if('TELEGRAM' in parser):
        telegram.api = parser['TELEGRAM']['BOT_TOKEN']
        telegram.auto_approve = parser.getboolean('TELEGRAM', 'AUTO_APPROVE')
        telegram.initialize()
        logger.info(__name__, "Telegram API initialized")
    else:
        logger.error(__name__, "Failed to initialize Telegram's API: Check your config.ini")
        exit()
