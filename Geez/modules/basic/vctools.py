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
from random import randint
from typing import Optional
from contextlib import suppress

from pyrogram import Client, enums, filters
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.messages import GetFullChat
from pyrogram.raw.functions.phone import CreateGroupCall, DiscardGroupCall
from pyrogram.raw.types import InputGroupCall, InputPeerChannel, InputPeerChat
from pyrogram.types import Message
from pyrogram.types import Message
from geezlibs.geez.helper import edit_or_reply
from geezlibs.geez.helper import get_arg
from Geez.helper.cmd import *
from Geez.modules.basic import add_command_help, DEVS
from Geez import SUDO_USER

async def get_group_call(
    client: Client, message: Message, err_msg: str = ""
) -> Optional[InputGroupCall]:
    chat_peer = await client.resolve_peer(message.chat.id)
    if isinstance(chat_peer, (InputPeerChannel, InputPeerChat)):
        if isinstance(chat_peer, InputPeerChannel):
            full_chat = (
                await client.invoke(GetFullChannel(channel=chat_peer))
            ).full_chat
        elif isinstance(chat_peer, InputPeerChat):
            full_chat = (
                await client.invoke(GetFullChat(chat_id=chat_peer.chat_id))
            ).full_chat
        if full_chat is not None:
            return full_chat.call
    await message.edit(f"**No group call Found** {err_msg}")
    return False


@Client.on_message(
    filters.command("startvcs", [cmd]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["startvc"], cmd) & filters.me)
async def opengc(client: Client, message: Message):
    flags = " ".join(message.command[1:])
    tex = await message.reply_text(message, "`Processing . . .`")
    vctitle = get_arg(message)
    if flags == enums.ChatType.CHANNEL:
        chat_id = message.chat.title
    else:
        chat_id = message.chat.id
    args = f"**Started Group Call\n • **Chat ID** : `{chat_id}`"
    try:
        if not vctitle:
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                )
            )
        else:
            args += f"\n • **Title:** `{vctitle}`"
            await client.invoke(
                CreateGroupCall(
                    peer=(await client.resolve_peer(chat_id)),
                    random_id=randint(10000, 999999999),
                    title=vctitle,
                )
            )
        await tex.edit(args)
    except Exception as e:
        await tex.edit(f"**INFO:** `{e}`")


@Client.on_message(
    filters.command("stopvcs", [cmd]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["stopvc"], cmd) & filters.me)
async def end_vc_(client: Client, message: Message):
    chat_id = message.chat.id
    if not (
        group_call := (
            await get_group_call(client, message, err_msg=", group call already ended")
        )
    ):
        return
    await client.invoke(DiscardGroupCall(call=group_call))
    await message.reply_text(f"Ended group call in **Chat ID** : `{chat_id}`")

@Client.on_message(
    filters.command("joinvcs", [cmd]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["joinvc"], cmd) & filters.me)
async def joinvc(client: Client, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client.me.id:
        Man = await message.reply("`Otw Naik...`")
    else:
        Man = await message.edit("`Otw Naik....`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.start(chat_id)
    except Exception as e:
        return await Man.edit(f"**ERROR:** `{e}`")
    await Man.edit(f"🤖 **Berhasil Join Ke Obrolan Group**\n└ **Chat ID:** `{chat_id}`")
    await asyncio.sleep(5)
    await client.group_call.set_is_mute(True)

@Client.on_message(
    filters.command("leavevcs", [cmd]) & filters.user(DEVS) & ~filters.me
)
@Client.on_message(filters.command(["leavevc"], cmd) & filters.me)
async def leavevc(client: Client, message: Message):
    chat_id = message.command[1] if len(message.command) > 1 else message.chat.id
    if message.from_user.id != client.me.id:
        Man = await message.reply("`Turun Dulu...`")
    else:
        Man = await message.edit("`Turun Dulu....`")
    with suppress(ValueError):
        chat_id = int(chat_id)
    try:
        await client.group_call.stop()
    except Exception as e:
        return await edit_or_reply(message, f"**ERROR:** `{e}`")
    msg = "🤖 **Berhasil Turun dari Obrolan Suara**"
    if chat_id:
        msg += f"\n└ **Chat ID:** `{chat_id}`"
    await Man.edit(msg)


add_command_help(
    "Vctools",
    [
        ["startvc", "Start voice chat of group."],
        ["stopvc", "End voice chat of group."],
        ["joinvcvc", "Join voice chat of group."],
        ["leavevc", "Leavevoice chat of group."],
    ],
)

