from backend.api import plex
from backend.database.statement import select
from backend import logger, constants
import telegram

def healthCheck(bot, job):
    if(plex.enabled):
        checkPlex(bot, job)

def checkPlex(bot, job):
    version = plex.getVersion()
    if(version):
        if(not plex.state):
            plex.state = True
            logger.info(__name__, constants.STATUS_PLEX_WENT_ONLINE[1:-1], "INFO_GREEN")
            if(plex.notification):
                admins = select.getAdmins()
                for admin in admins:
                    bot.send_message(chat_id=admin, text=constants.STATUS_PLEX_WENT_ONLINE, parse_mode=telegram.ParseMode.MARKDOWN)
    else:
        if(plex.state):
            plex.state = False
            logger.error(__name__, constants.STATUS_PLEX_WENT_OFFLINE[1:-1])
            if(plex.notification):
                admins = select.getAdmins()
                for admin in admins:
                    bot.send_message(chat_id=admin, text=constants.STATUS_PLEX_WENT_OFFLINE, parse_mode=telegram.ParseMode.MARKDOWN)
