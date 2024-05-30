
import logging
import time
import sys

from pyrogram import Client

from telethon.sessions import StringSession
from telethon.sync import TelegramClient

from decouple import config

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)
logging.getLogger("pyrogram").setLevel(logging.WARNING)
logging.getLogger("telethon").setLevel(logging.WARNING)


# ---------------------------
# variables
# ---------------------------

API_ID = config("API_ID", default=None, cast=int)
API_HASH = config("API_HASH", default=None)
BOT_TOKEN = config("BOT_TOKEN", default=None)
SESSION = config("SESSION", default=None)
FORCESUB = config("FORCESUB", default=None)
AUTH = config("AUTH", default=None)
SUDO_USERS = []

if len(AUTH) != 0:
    SUDO_USERS = {int(AUTH.strip()) for AUTH in AUTH.split()}
else:
    SUDO_USERS = set()


# ---------------------------
# TelethonBot
# ---------------------------

bot = TelegramClient('TelethonBot', API_ID, API_HASH).start(bot_token=BOT_TOKEN)

# ---------------------------
# UserBot
# ---------------------------
userbot = Client("UserBot",api_id=API_ID,api_hash=API_HASH,session_string=SESSION)

try:
    userbot.start()

except BaseException:
    print("Userbot Error ! Have you added SESSION while deploying??")
    sys.exit(1)


# ---------------------------
# PyrogramBot
# ---------------------------

Bot = Client(
    "PyrogramBot",
    bot_token=BOT_TOKEN,
    api_id=int(API_ID),
    api_hash=API_HASH
)

try:
    Bot.start()
except Exception as e:
    #print(e)
    logger.info(e)
    sys.exit(1)
