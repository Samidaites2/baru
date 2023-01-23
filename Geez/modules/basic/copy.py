import asyncio
import os
from pyrogram.types import *
from pyrogram import *
from pyrogram import Client as gez
from pyrogram import Client
from Geez.helper.cmd import *
from geezlibs.geez.helper.basic import *
from geezlibs.geez.helper.PyroHelpers import *
from geezlibs.geez.utils.misc import *
from geezlibs.geez.utils.tools import *


@gez.on_message(filters.command("copy", cmd) & filters.me)
async def kangcopy(client: Client, message: Message):
    link = get_arg(message)
bot = "kangcopybot"
if link:
     try:
         await client.send_message(bot, link)
         await asyncio.sleep(2)
         async for ren in client.get_history(bot, limit=1):
             await ren.copy(message.chat.id)
      except:
         pass

add_command_help(
    "Curi",
    [
        [f"copy <link>", "Nyolong Media/Foto."],
    ],
)
