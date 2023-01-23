# if you can read this, this meant you use code from Geez Ram Project
# this code is from somewhere else
# please dont hestitate to steal it
# because Geez and Ram doesn't care about credit
# at least we are know as well
# who Geez and Ram is
#
#
# kopas repo dan hapus credit, ga akan jadikan lu seorang developer
# ©2023 Geez & Ram Team

from pyrogram import Client, enums, filters
from pyrogram.types import Message

from Geez.database.notesdb import *
from Geez import *
from geezlibs.geez.helper import *
from geezlibs.geez.utils import *

BOTLOG_CHATID = "-1001774571904"


@Client.on_message(filters.command(["save"], cmd) & filters.me)
async def notes(client: Client, message: Message):
    note_ = await edit_or_reply(message, "`Processing...`")
    note_name = get_text(message)
    if not note_name:
        await note_.edit("`Mohon berikan judul ke pesan...`")
        return
    if not message.reply_to_message:
        await note_.edit("`Mohon balas ke pesan...`")
        return
    note_name = note_name.lower()
    msg = message.reply_to_message
    copied_msg = await msg.copy(int(BOTLOG_CHATID))
    await add_note(note_name, message.chat.id, copied_msg.message_id)
    await note_.edit("`Added To My Database.`")


@Client.on_message(filters.command(["get"], cmd) & filters.me)
async def lmao(client: Client, message: Message):
    if not await all_note(message.chat.id):
        return
    owo = message.matches[0].group(1)
    if owo is None:
        return
    if await note_info(owo, message.chat.id):
        sed = await note_info(owo, message.chat.id)
        await client.copy_message(
            from_chat_id=int(BOTLOG_CHATID),
            chat_id=message.chat.id,
            message_id=sed["msg_id"],
            reply_to_message_id=message.message_id,
        )
    
