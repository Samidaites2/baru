from pyrogram import filters, Client
import asyncio
from pyrogram.types import Message 
from pyrogram.methods import messages
from geezlibs.geez.database.pmpermitdb import *
from geezlibs.geez.database import *
from Geez.helper.cmd import *
import geezlibs.geez.database.pmpermitdb as TOD
from config import BOTLOG_CHATID

FLOOD_CTRL = 0
ALLOWED = []
USERS_AND_WARNS = {}
flood = {}


async def denied_users(filter, client: Client, message: Message):
    if not await pm_guard():
        return False
    if message.chat.id in (await is_pmpermit_approved()):
        return False
    else:
        return True

def get_arg(message):
    msg = message.text
    msg = msg.replace(" ", "", 1) if msg[1] == " " else msg
    split = msg[1:].replace("\n", " \n").split(" ")
    if " ".join(split[1:]).strip() == "":
        return ""
    return " ".join(split[1:])


@Client.on_message(filters.command(["allow", "ok", "approve", "k"], cmd) & filters.me & filters.private)
async def pm_approve(client, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Reply to a user's message to approve."
        )
    user_id = message.reply_to_message.from_user.id
    if await is_pmpermit_approved(user_id):
        return await eor(message, text="User is already approved to pm")
    await approve_pmpermit(user_id)
    await eor(message, text="User is approved to pm")


@Client.on_message(filters.command(["no", "tolak", "disapprove", "blok"], cmd) & filters.me & filters.private)
async def pm_disapprove(client, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Reply to a user's message to disapprove."
        )
    user_id = message.reply_to_message.from_user.id
    if not await is_pmpermit_approved(user_id):
        await eor(message, text="User is already disapproved to pm")
        async for m in client.iter_history(user_id, limit=6):
            if m.reply_markup:
                try:
                    await m.delete()
                except Exception:
                    pass
        return
    await disapprove_pmpermit(user_id)
    await eor(message, text="User is disapproved to pm")
    
    
@Client.on_message(filters.command(["blok"], cmd) & filters.me & filters.private)
async def block_user_func(client, message):
    if not message.reply_to_message:
        return await eor(message, text="Reply to a user's message to block.")
    user_id = message.reply_to_message.from_user.id
    await eor(message, text="Successfully blocked the user")
    await client.block_user(user_id)


@Client.on_message(filters.command(["unblock"], cmd) & filters.me & filters.private)
async def unblock_user_func(client, message):
    if not message.reply_to_message:
        return await eor(
            message, text="Reply to a user's message to unblock."
        )
    user_id = message.reply_to_message.from_user.id
    await client.unblock_user(user_id)
    await eor(message, text="Successfully Unblocked the user")


@Client.on_message(
    filters.private
    & filters.incoming
    & ~filters.service
    & ~filters.me
    & ~filters.bot
)
async def awaiting_message(client, message):
    if await is_on_off(5):
        try:
            await client.forward_messages(
                chat_id=BOTLOG_CHATID,
                from_chat_id=message.from_user.id,
                message_ids=message.message_id,
            )
        except Exception as err:
            pass
    user_id = message.from_user.id
    if await is_pmpermit_approved(user_id):
        return
    async for m in client.iter_history(user_id, limit=6):
        if m.reply_markup:
            await m.delete()
    if str(user_id) in flood:
        flood[str(user_id)] += 1
    else:
        flood[str(user_id)] = 1
    if flood[str(user_id)] > 5:
        await message.reply_text("Spam Detected. User Blocked")
        await client.send_message(
            BOTLOG_CHATID,
            f"**Spam Detect Block**\n\n- **Blocked User:** {message.from_user.mention}\n- **User ID:** {message.from_user.id}",
        )
        return await client.block_user(user_id)
    await message.reply_text(
        f"**peringatan! tolong baca pesan ini dengan hati-hati..\n\n**"
    "**Saya Premium Userbot, saya di sini untuk melindungi tuanku dari spam**"
    "**jika Anda bukan spammer, harap tunggu!.\n\n**"
    "**sampai saat itu, jangan spam atau Anda akan diblokir dan dilaporkan bb saya, jadi berhati-hatilah untuk mengirim pesan pesan!**"
    )
