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
import asyncio
from pyrogram import Client, filters
from pyrogram.types import Message
from geezlibs.geez.helper.basic import edit_or_reply
from geezlibs.geez.helper.PyroHelpers import ReplyCheck
from Geez.helper.cmd import *
from Geez.modules.basic import add_command_help


@Client.on_message(filters.command("p", cmd) & filters.me)
async def salamone(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "Assalamualaikum...",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@Client.on_message(filters.command("pe", cmd) & filters.me)
async def salamdua(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "Assalamualaikum Warahmatullahi Wabarakatuh",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@Client.on_message(filters.command("l", cmd) & filters.me)
async def jwbsalam(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "Wa'alaikumsalam...",
            reply_to_message_id=ReplyCheck(message),
        ),
    )


@Client.on_message(filters.command("el", cmd) & filters.me)
async def jwbsalamlngkp(client: Client, message: Message):
    await asyncio.gather(
        message.delete(),
        client.send_message(
            message.chat.id,
            "Wa'alaikumsalam Warahmatullahi Wabarakatuh",
            reply_to_message_id=ReplyCheck(message),
        ),
    )



@Client.on_message(filters.command("ass", cmd) & filters.me)
async def salamarab(client: Client, message: Message):
    xx = await edit_or_reply(message, "Salam Dulu Gua..")
    await asyncio.sleep(2)
    await xx.edit("السَّلاَمُ عَلَيْكُمْ وَرَحْمَةُ اللهِ وَبَرَكَاتُهُ")

add_command_help(
    "Salam",
    [
        ["p", "Assalamualaikum."],
        ["pe", "Assalamualaikum Warahmatullahi Wabarakatuh."],
        ["l", "Wa'alaikumsalam."],
        ["ass", "Assalamualaikum Bahas arab."],
    ]
)