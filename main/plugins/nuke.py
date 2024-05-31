import os

from telethon import events
from main.__init__ import bot as TelethonBot
from main.__init__ import SUDO_USERS

# ----------------------
# Nuke (restart bot)
# ----------------------

@TelethonBot.on(
    events.NewMessage(incoming=True,
                      #from_users=AUTH,
                      from_users=SUDO_USERS,
                      pattern="/nuke",
                      func=lambda e: e.is_private))
async def shutdown(event):
    await event.reply("Exited.")
    os._exit(1)
