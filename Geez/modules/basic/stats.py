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
from datetime import datetime
from pyrogram import Client, enums, filters
from pyrogram.types import Message
from Geez.modules.basic import *
from Geez import cmds

@Client.on_message(filters.command(["stats", "status"], cmds) & filters.me)
async def stats(client: Client, message: Message):
    Man = await message.edit_text("`Collecting stats...`")
    start = datetime.now()
    u = 0
    g = 0
    sg = 0
    c = 0
    b = 0
    a_chat = 0
    Meh = await client.get_me()
    async for dialog in client.get_dialogs():
        if dialog.chat.type == enums.ChatType.PRIVATE:
            u += 1
        elif dialog.chat.type == enums.ChatType.BOT:
            b += 1
        elif dialog.chat.type == enums.ChatType.GROUP:
            g += 1
        elif dialog.chat.type == enums.ChatType.SUPERGROUP:
            sg += 1
            user_s = await dialog.chat.get_member(int(Meh.id))
            if user_s.status in (
                enums.ChatMemberStatus.OWNER,
                enums.ChatMemberStatus.ADMINISTRATOR,
            ):
                a_chat += 1
        elif dialog.chat.type == enums.ChatType.CHANNEL:
            c += 1

    end = datetime.now()
    ms = (end - start).seconds
    await Man.edit_text(
        """`Your Stats Obtained in {} seconds`
`You have {} Private Messages.`
`You are in {} Groups.`
`You are in {} Super Groups.`
`You Are in {} Channels.`
`You Are Admin in {} Chats.`
`Bots = {}`""".format(
            ms, u, g, sg, c, a_chat, b
        )
    )


add_command_help(
    "Stats",
    [
        [f"{cmds}stats", "to check your account status."],
    ],
)
