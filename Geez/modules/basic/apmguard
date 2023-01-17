
import asyncio
from pyrogram.methods import messages
from pyrogram import filters, Client
import geezlibs.geez.database.pmpermitdb as TOD
from Geez import SUDO_USER
from Geez.helper.cmd import *
from Geez.modules.basic.help import *
from .pmguard import get_arg, denied_users





@Client.on_message(filters.command("pm", cmd) & filters.me)
async def pmguard(client, message):
    arg = get_arg(message)
    if not arg:
        await message.edit("**I only understand True or False**")
        return
    if arg == "False":
        await TOD.add_off(False)
        await message.edit("**PM Guard Deactivated**")
    if arg == "True":
        await TOD.add_on(True)
        await message.edit("**PM Guard Activated**")



add_command_help(
    "PM",
    [
        ["pm [on or off]", " -> Activates or deactivates anti-pm."],
        ["block", " -> Block a user to you."],
        ["unblock", " -> Unblock a user to you."],
        ["ok", " -> Allows a user to PM you."],
        ["no", " -> Denies a user to PM you."],
    ],
)
