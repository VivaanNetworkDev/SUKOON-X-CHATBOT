import asyncio
import random

from pyrogram import filters
from pyrogram.types import InlineKeyboardMarkup, Message
from pyrogram.enums import ChatType

from SUKOONXCHATBOT import app
from SUKOONXCHATBOT.database.chats import add_served_chat
from SUKOONXCHATBOT.database.users import add_served_user
from SUKOONXCHATBOT.modules.helpers import (
    CLOSE_BTN,
    DEV_OP,
    HELP_BTN,
    HELP_BUTN,
    HELP_READ,
    HELP_START,
    SOURCE_READ,
    START,
)


# Random start videos
SUKOON_VID = [
    "https://telegra.ph/file/9b7e1b820c72a14d90be7.mp4",
    "https://telegra.ph/file/a4d90b0cb759b67d68644.mp4",
    "https://telegra.ph/file/72f349b1386d6d9374a38.mp4",
    "https://telegra.ph/file/2b75449612172a96d4599.mp4",
    "https://telegra.ph/file/b3ac2d77205d5ded860de.mp4",
    "https://telegra.ph/file/58ae4ac86ef70dc8c8f6a.mp4",
    "https://telegra.ph/file/c6c1ac9aee4192a8a3747.mp4",
    "https://telegra.ph/file/55c840c8eba0555318f0d.mp4",
    "https://telegra.ph/file/e97715885d0a0cfbddaaa.mp4",
    "https://telegra.ph/file/943bb99829ec526c3f99a.mp4"
]

# Random stickers
STICKER = [
    "CAACAgUAAx0CYlaJawABBy4vZaieO6T-Ayg3mD-JP-f0yxJngIkAAv0JAALVS_FWQY7kbQSaI-geBA",
    "CAACAgUAAx0CYlaJawABBy4rZaid77Tf70SV_CfjmbMgdJyVD8sAApwLAALGXCFXmCx8ZC5nlfQeBA",
    "CAACAgUAAx0CYlaJawABBy4jZaidvIXNPYnpAjNnKgzaHmh3cvoAAiwIAAIda2lVNdNI2QABHuVVHgQ",
]

# Random emojis
EMOJIOS = ["💣", "💥", "🪄", "🧨", "⚡", "🤡", "👻", "🎃", "🎩", "🕊"]


# Command handler for /start and /aistart
@app.on_cmd(["start", "aistart"])
async def start_command_handler(_, m: Message):
    if m.chat.type == ChatType.PRIVATE:
        # Display loading messages
        accha = await m.reply_text(text=random.choice(EMOJIOS))
        await asyncio.sleep(1.3)
        await accha.edit("🏓𝐒ᴜᴋᴏᴏɴ..ᴍᴇᴇɴʏ..ᴍɪɴʏ..ᴍᴏᴇ✨")
        await asyncio.sleep(0.2)
        await accha.edit("__𝐒ᴜᴋᴏᴏɴ..ᴍᴇᴇɴʏ ꨄ sтαятιиg.....__")
        await asyncio.sleep(0.2)
        await accha.edit("__𝓢𝓾𝓴𝓸𝓸𝓷 sтαятιиg..__")
        await asyncio.sleep(0.2)
        await accha.delete()

        # Send a random sticker
        umm = await m.reply_sticker(sticker=random.choice(STICKER))
        await asyncio.sleep(2)
        await umm.delete()

        # Send a random video with a caption
        await m.reply_video(
            video=random.choice(SUKOON_VID),
            caption=f"""**๏ ʜᴇʏ, ɪ ᴀᴍ {app.name}**\n**➻ ᴀɴ ᴀɪ ʙᴀsᴇᴅ ᴄʜᴀᴛʙᴏᴛ.**\n**──────────────**\n**➻ ᴜsᴀɢᴇ /chatbot [ᴏɴ/ᴏғғ]**\n<b>๏ ʜɪᴛ ʜᴇʟᴘ ʙᴜᴛᴛᴏɴ ғᴏʀ ʜᴇʟᴘ</b>""",
            reply_markup=InlineKeyboardMarkup(DEV_OP),
        )
        await add_served_user(m.from_user.id)
    else:
        await m.reply_video(
            video=random.choice(SUKOON_VID),
            caption=START,
            reply_markup=InlineKeyboardMarkup(HELP_START),
        )
        await add_served_chat(m.chat.id)


# Command handler for /help
@app.on_cmd("help")
async def help_command_handler(_, m: Message):
    if m.chat.type == ChatType.PRIVATE:
        hmm = await m.reply_video(
            video=random.choice(SUKOON_VID),
            caption=HELP_READ,
            reply_markup=InlineKeyboardMarkup(HELP_BTN),
        )
        await add_served_user(m.from_user.id)
    else:
        await m.reply_video(
            video=random.choice(SUKOON_VID),
            caption="**ʜᴇʏ, ᴘᴍ ᴍᴇ ғᴏʀ ʜᴇʟᴘ ᴄᴏᴍᴍᴀɴᴅs!**",
            reply_markup=InlineKeyboardMarkup(HELP_BUTN),
        )
        await add_served_chat(m.chat.id)


# Command handler for /repo
@app.on_cmd("repo")
async def repo_command_handler(_, m: Message):
    await m.reply_text(
        text=SOURCE_READ,
        reply_markup=InlineKeyboardMarkup(CLOSE_BTN),
        disable_web_page_preview=True,
    )

##########################################################
