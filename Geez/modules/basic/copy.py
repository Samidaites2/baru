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
    mmk = await message.reply_text("`Processing . . .`")
    link = get_arg(message)
    bot = "kangcopybot"
    if link:
        try:
            await asyncio.sleep(1.5)
        except Exception as e:
            return await mmk.edit(message, f"**ERROR:** `{e}`")
        try:
            await asyncio.sleep(1.5)
            tai = await mmk.edit("`Nyolong berhasil...`")
            a = await client.send_message(bot, link)
            await asyncio.sleep(2)
            await a.delete()
            await tai.delete()
            async for c in client.get_chat_history(bot, limit=1):
                await c.copy(message.chat.id)
        except BaseException:
            pass
        try:
            async for f in client.search_messages(message.chat.id, query="Trying to Download."):
                await f.delete()
            async for o in client.search_messages(message.chat.id, query="DOWNLOADING:"):
                await o.delete()
            async for g in client.search_messages(message.chat.id, query="Preparing to Upload!"):
                await g.delete()
        except BaseException:
            pass

add_command_help(
    "Curi",
    [
        [f"copy <link>", "Nyolong Media/Foto."],
    ],
)
