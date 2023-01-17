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
from geezlibs import DEVS, BL_GEEZ
from geezlibs.geez.helper.PyroHelpers import get_ub_chats
from Geez.modules.basic.profile import extract_user, extract_user_and_reason
from Geez.helper.cmd import *
from geezlibs.geez.database import gbandb as Geez
from geezlibs.geez.database import gmutedb as Gmute
from Geez.modules.basic import add_command_help

ok = []

@Client.on_message(
    filters.command("cgban", cmd) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("gban", cmd) & filters.me)
async def gban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        ex = await message.reply_text("`Gbanning...`")
    else:
        ex = await message.edit("`Gbanning....`")
    if not user_id:
        return await ex.edit("I can't find that user.")
    if user_id == client.me.id:
        return await ex.edit("**Okay Done... 🐽**")
    if user_id in DEVS:
        return await ex.edit("**Baap ko Mat sikha 🗿**")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await ex.edit("`Please specify a valid user!`")

    if (await Geez.gban_info(user.id)):
        return await ex.edit(
            f"[user](tg://user?id={user.id}) **it's already on the gbanned list**"
        )
    f_chats = await get_ub_chats(client)
    if not f_chats:
        return await ex.edit("**You don't have a GC that you admin 🥺**")
    er = 0
    done = 0
    for gokid in f_chats:
        try:
            await client.ban_chat_member(chat_id=gokid, user_id=int(user.id))
            done += 1
        except BaseException:
            er += 1
    await Geez.gban_user(user.id)
    ok.append(user.id)
    msg = (
        r"**\\#GBanned_User//**"
        f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})"
        f"\n**User ID:** `{user.id}`"
    )
    if reason:
        msg += f"\n**Reason:** `{reason}`"
    msg += f"\n**Affected To:** `{done}` **Chats**"
    await ex.edit(msg)


@Client.on_message(
    filters.command("cungban", cmd) & filters.user(DEVS) & ~filters.via_bot
)
@Client.on_message(filters.command("ungban", cmd) & filters.me)
async def ungban_user(client: Client, message: Message):
    user_id, reason = await extract_user_and_reason(message, sender_chat=True)
    if message.from_user.id != client.me.id:
        ex = await message.reply("`UnGbanning...`")
    else:
        ex = await message.edit("`UnGbanning....`")
    if not user_id:
        return await ex.edit("I can't find that user.")
    if user_id:
        try:
            user = await client.get_users(user_id)
        except Exception:
            return await ex.edit("`Please specify a valid user!`")

    try:
        if not (await Geez.gban_info(user.id)):
            return await ex.edit("`User already ungban`")
        ung_chats = await get_ub_chats(client)
        ok.remove(user.id)
        if not ung_chats:
            return await ex.edit("**You don't have a Group that you admin 🥺**")
        er = 0
        done = 0
        for good_boi in ung_chats:
            try:
                await client.unban_chat_member(chat_id=good_boi, user_id=user.id)
                done += 1
            except BaseException:
                er += 1
        await Geez.ungban_user(user.id)
        msg = (
            r"**\\#UnGbanned_User//**"
            f"\n\n**First Name:** [{user.first_name}](tg://user?id={user.id})"
            f"\n**User ID:** `{user.id}`"
        )
        if reason:
            msg += f"\n**Reason:** `{reason}`"
        msg += f"\n**Affected To:** `{done}` **Chats**"
        await ex.edit(msg)
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@Client.on_message(filters.command("listgban", cmd) & filters.me)
async def gbanlist(client: Client, message: Message):
    users = (await Geez.gban_list())
    oof = "**GBanned Users:**\n"
    ex = await message.edit_text("`Processing...`")
    list_ = await Geez.gban_list()
    if len(list_) == 0:
        await ex.edit("**No Users have been Banned yet**")
        return
    for lit in list_:
        oof += f"**User :** `{lit['user']}` \n**Reason :** `{lit['reason']}` \n\n"
    return await ex.edit(gban_list)


@Client.on_message(filters.command("gmute", cmd) & filters.me)
async def gmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.edit_text(message, "`Processing...`")
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
    if user.id in DEVS:
        return await ex.edit("**Baap Ko mat sikha 🗿**")
    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await ex.edit("`Calm down anybob, you can't gmute yourself.`")
    except BaseException:
        pass

    try:
        if (await Gmute.is_gmuted(user.id)):
            return await ex.edit("`User already gmuted`")
        await Gmute.gmute(user.id)
        ok.append(user.id)
        await ex.edit(f"[{user.first_name}](tg://user?id={user.id}) globally gmuted!")
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.restrict_member(user.id, ChatPermissions())
        except BaseException:
            pass
    
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


@Client.on_message(filters.command("ungmute", cmd) & filters.me)
async def ungmute_user(client: Client, message: Message):
    args = await extract_user(message)
    reply = message.reply_to_message
    ex = await message.edit_text("`Processing...`")
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

    try:
        replied_user = reply.from_user
        if replied_user.is_self:
            return await ex.edit("`Calm down anybob, you can't ungmute yourself.`")
    except BaseException:
        pass

    try:
        if not (await Gmute.is_gmuted(user.id)):
            return await ex.edit("`User already ungmuted`")
        await Gmute.ungmute(user.id)
        ok.remove(user.id)
        try:
            common_chats = await client.get_common_chats(user.id)
            for i in common_chats:
                await i.unban_member(user.id)
        except BaseException:
            pass
        await ex.edit(
            f"[{user.first_name}](tg://user?id={user.id}) globally ungmuted!"
        )
    except Exception as e:
        await ex.edit(f"**ERROR:** `{e}`")
        return


add_command_help(
    "Global",
    [
        [
            "gban <reply/username/userid>",
            "Do Global Banned To All Groups Where You As Admin.",
        ],
        ["ungban <reply/username/userid>", "Remove Global Banned."],
        ["listgban", "Displays the Global Banned List."],
    ],
)
