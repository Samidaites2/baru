import importlib
import time
from pyrogram import idle
from uvloop import install
from geezlibs import join
from geezlibs import BOT_VER, __version__ as gver
from Geez import BOTLOG_CHATID, LOGGER, LOOP, aiosession, bot1, bots, app, ids
from config import CMD_HNDLR
from Geez.modules import ALL_MODULES


MSG_ON = """
**Premium Userbot Actived ✅**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
**Userbot Version -** `{}`
**Ketik** `{}alive` **untuk Mengecheck Bot**
╼┅━━━━━━━━━━╍━━━━━━━━━━┅╾
"""
MSG_BOT = (f"**Userbot Assistant**\nis alive...")




async def main():
    await app.start()
    await app.run()
    LOGGER("✅").info(" Premium Userbot..")
    LOGGER("✅").info("Loading Everything.")
    for all_module in ALL_MODULES:
        importlib.import_module("Geez.modules" + all_module)
        LOGGER("✅").info(f"Successfully Imported {all_module} ")
    for bot in bots:
        try:
            await bot.start()
            ex = await bot.get_me()
            await join(bot)
            try:
                await bot.send_message(BOTLOG_CHATID, MSG_ON.format(BOT_VER, CMD_HNDLR))
                await app.send_message(BOTLOG_CHATID, MSG_BOT)
            except BaseException as a:
                LOGGER("✅").warning(f"{a}")
            LOGGER("✅").info(f"Started as {ex.first_name} | {ex.id} ")
            ids.append(ex.id)
        except Exception as e:
            LOGGER("✅").info(f"{e}")
    await idle()
    await aiosession.close()


if __name__ == "__main__":
    LOGGER("✅").info("Starting Premium Userbot")
    install()
    LOOP.run_until_complete(main())

