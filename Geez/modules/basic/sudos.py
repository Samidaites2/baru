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
from pyrogram import Client, errors, filters
from pyrogram.types import ChatPermissions, Message
from geezlibs.geez.helper.PyroHelpers import get_ub_chats
from Geez.modules.basic.profile import extract_user, extract_user_and_reason
from Geez import SUDO_USER
from config import OWNER_ID
from Geez.modules.basic import add_command_help
from Geez import cmds

ok = []

@Client.on_message(filters.command("sudolist", cmds) & filters.me)
async def sudolist(client: Client, message: Message):
    users = (SUDO_USER)
    ex = await message.edit_text("`Processing...`")
    if not users:
        return await ex.edit("No Users have been set yet")
    gban_list = "**Sudo Users:**\n"
    count = 0
    for i in users:
        count += 1
        gban_list += f"**{count} -** `{i}`\n"
    return await ex.edit(gban_list)


@Client.on_message(filters.command("addsudo", cmds) & filters.user(OWNER_ID))
async def addsudo(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.reply_text("`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await ex.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await ex.edit(f"`Please specify a valid user!`")
        return
    if user.id == client.me.id:
        return await ex.edit("**Okay Sure.. 🐽**")

    try:
        if user.id in SUDO_USER:
            return await ex.edit("`User already in sudo`")
        SUDO_USER.append(user.id)
        await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) Added To Sudo Users!")
    
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@Client.on_message(filters.command("rmsudo", cmds) & filters.user(OWNER_ID))
async def rmsudo(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.reply_text("`Processing...`")
    if args:
        try:
            user = await client.get_users(args)
        except Exception:
            await ex.edit(f"`Please specify a valid user!`")
            return
    elif reply:
        user_id = reply.from_user.id
        user = await client.get_users(user_id)
    else:
        await ex.edit(f"`Please specify a valid user!`")
        return
    if user.id == client.me.id:
        return await ex.edit("**Okay Sure.. 🐽**")

    try:
        if user.id in SUDO_USER:
            return await ex.edit("`User is not a part of sudo`")
        SUDO_USER.remove(user.id)
        await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) Removed To Sudo Users!")
    
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return
