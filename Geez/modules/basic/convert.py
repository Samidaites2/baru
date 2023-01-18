from pyrogram import Client, filters
from pyrogram.enums import MessageMediaType
from pyrogram.types import Message

from geezlibs.geez.helper.PyroHelpers import ReplyCheck
from geezlibs.geez.utils.tools import *
from Geez.helper.cmd import *
from Geez.modules.basic import add_command_help


@Client.on_message(
    filters.command("audio", cmd) & filters.me
)
async def extract_audio(client: Client, message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("**Mohon Balas Ke Video**")
        return
    if replied.media == MessageMediaType.VIDEO:
        await message.reply("`Downloading Video . . .`")
        file = await client.download_media(
            message=replied,
            file_name="cache/dowloads/{out_file}",
        )
        replied.video.duration
        out_file = file + ".mp3"
        try:
            xx = await message.reply("`Trying Extract Audio. . .`")
            bash = f"ffmpeg -i {file} -q:a 0 -map a {out_file}"
            await bash(cmd)
            await xx.edit("`Uploading Audio . . .`")
            await xx.delete()
            await client.send_audio(
                message.chat.id,
                audio=out_file,
                reply_to_message_id=ReplyCheck(message),
            )
        except BaseException as e:
            await message.reply(f"**INFO:** `{out_file}`")
    else:
        await message.reply("**Mohon Balas Ke Video**")
        return


@Client.on_message(filters.command("makevoice", cmd) & filters.me)
async def makevoice(client: Client, message: Message):
    replied = message.reply_to_message
    if not replied:
        await message.reply("**Mohon Balas Ke Audio atau video**")
        return
    if replied.media == MessageMediaType.VIDEO or MessageMediaType.AUDIO:
        await message.reply("`Downloading . . .`")
        file = await client.download_media(
            message=replied,
            file_name="cache/dowloads/{file}",
        )
        if replied.video:
            replied.video.duration
        else:
            if replied.audio:
                replied.audio.duration
            if replied.voice:
                replied.voice.duration
        try:
            xx = await message.reply("`Trying Make Audio . . .`")
            bash = f"ffmpeg -i '{file}' -map 0:a -codec:a libopus -b:a 100k -vbr on voice.opus"
            await bash(cmd)
            await xx.edit("`Uploading Audio . . .`")
            await xx.delete()
            await client.send_voice(
                message.chat.id,
                voice="voice.opus",
                reply_to_message_id=ReplyCheck(message),
            )
        except BaseException as e:
            await message.reply(f"**INFO:** `{voice}`")
    else:
        await message.reply("**Mohon Balas Ke Audio atau video**")
        return


add_command_help(
    "Convert",
    [
        ["audio <reply to file>", "Convert video to audio"],
        ["makevoice <reply to file>", "make voive video and audio"],
    ],
)
