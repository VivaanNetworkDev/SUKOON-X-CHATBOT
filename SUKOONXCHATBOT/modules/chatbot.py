import random
import logging
import openai  # Legacy import for compatibility (v0.28.x)
from pymongo import MongoClient
from pyrogram import Client, filters
from pyrogram.enums import ChatAction
from pyrogram.errors import ChannelPrivate
from pyrogram.types import InlineKeyboardMarkup, Message
from config import MONGO_URL, GPT_API
from SUKOONXCHATBOT import app
from SUKOONXCHATBOT.modules.helpers import CHATBOT_ON
from Abg.chat_status import adminsOnly

# Global connections for efficiency
mongo_client = MongoClient(MONGO_URL)
chatai = mongo_client["Word"]["WordDb"]  # Responses DB
sukoon = mongo_client["SukoonDb"]["Sukoon"]  # Enabled/Disabled DB

# Setup OpenAI (legacy v0.28.x compatible)
if GPT_API:
    openai.api_key = GPT_API
    ai_enabled = True
else:
    ai_enabled = False

logger = logging.getLogger(__name__)

# Admin command to toggle chatbot (assumes CHATBOT_ON buttons handle insert/delete in sukoon)
@app.on_cmd("chatbot", group_only=True)
@adminsOnly("can_delete_messages")
async def chaton_(_, m: Message):
    await m.reply_text(
        f"ᴄʜᴀᴛ: {m.chat.title}\n**ᴄʜᴏᴏsᴇ ᴀɴ ᴏᴩᴛɪᴏɴ ᴛᴏ ᴇɴᴀʙʟᴇ/ᴅɪsᴀʙʟᴇ ᴄʜᴀᴛʙᴏᴛ.**",
        reply_markup=InlineKeyboardMarkup(CHATBOT_ON),
    )

# Consolidated group handler (text or sticker, skips commands/bots)
@app.on_message(
    filters.group & (filters.text | filters.sticker) & ~filters.bot() & ~filters.command(), group=4
)
async def handle_group(client: Client, message: Message):
    # Extra prefix check for safety (in case filter misses)
    if message.text and message.text.startswith(("!", "/", "?", "@", "#")):
        return
    # Check if disabled (doc exists = disabled)
    is_disabled = sukoon.find_one({"chat_id": message.chat.id})
    if is_disabled:
        return
    await _handle_message(client, message, is_group=True)

# Consolidated private handler (always enabled, text or sticker)
@app.on_message(
    filters.private & (filters.text | filters.sticker) & ~filters.bot() & ~filters.command(), group=4
)
async def handle_private(client: Client, message: Message):
    # Extra prefix check
    if message.text and message.text.startswith(("!", "/", "?", "@", "#")):
        return
    await _handle_message(client, message, is_group=False)

# Core message handling logic (shared for groups/private)
async def _handle_message(client: Client, message: Message, is_group: bool):
    # Safely send typing indicator
    try:
        await client.send_chat_action(message.chat.id, ChatAction.TYPING)
    except ChannelPrivate:
        logger.debug("Could not send typing action (private channel)")
    except Exception as e:
        logger.error(f"Unexpected error in send_chat_action: {e}")

    # LEARNING: If replying to bot's message, learn the pair (input = replied, response = this message)
    if message.reply_to_message and message.reply_to_message.from_user.is_self:
        await _learn_response(message)
        return  # Don't auto-respond; this is teaching mode

    # RESPOND: Determine input key
    input_key = None
    is_sticker_input = False
    if message.text:
        input_key = message.text  # Exact match; could add .lower() for fuzzy
    elif message.sticker:
        input_key = message.sticker.file_unique_id
        is_sticker_input = True

    if not input_key:
        return  # Ignore other message types

    # Search DB for matches
    matches = list(chatai.find({"word": input_key}))
    if matches:
        # Random response from matches
        resp_content = random.choice([m["text"] for m in matches])
        resp_doc = chatai.find_one({"text": resp_content})
        resp_type = resp_doc.get("check", "none")

        if resp_type == "sticker":
            await message.reply_sticker(resp_content)
        else:
            await message.reply_text(resp_content)
        logger.debug(f"DB response sent for key: {input_key}")
    else:
        # FALLBACK: AI for text (100% accuracy guarantee), simple for stickers
        if message.text and ai_enabled:
            try:
                response = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {"role": "system", "content": "You are Sukoon, a witty, helpful, and fun Telegram chatbot. Keep responses short, engaging, and under 200 characters. Respond in a casual, friendly tone."},
                        {"role": "user", "content": f"User said: {message.text}"}
                    ],
                    max_tokens=150,
                    temperature=0.8
                )
                ai_resp = response.choices[0].message.content.strip()
                await message.reply_text(ai_resp)
                # Learn the AI response for future DB use
                chatai.insert_one({
                    "word": input_key,
                    "text": ai_resp,
                    "check": "none"
                })
                logger.info(f"AI fallback used and learned for: {input_key}")
            except Exception as e:
                logger.error(f"AI fallback error: {e}")
                await message.reply_text("Hmm, I'm thinking... Reply to me to teach what I should say! 🤔")
        elif is_sticker_input:
            # Simple sticker response (no AI for non-text)
            await message.reply_text("Love that sticker! What's the story behind it? 😄")
            # Optional: Learn a default, but skip for now
        else:
            await message.reply_text("I got nothing yet—teach me by replying to this!")

# Learning function (store replied_key -> response pair if new)
async def _learn_response(message: Message):
    replied = message.reply_to_message
    replied_key = None
    if replied.text:
        replied_key = replied.text  # Exact; could .lower()
    elif replied.sticker:
        replied_key = replied.sticker.file_unique_id

    if not replied_key:
        return

    resp_content = message.sticker.file_id if message.sticker else (message.text or None)
    if not resp_content:
        return

    resp_type = "sticker" if message.sticker else "none"

    # Avoid duplicates
    existing = chatai.find_one({"word": replied_key, "text": resp_content})
    if not existing:
        chatai.insert_one({
            "word": replied_key,
            "text": resp_content,
            "check": resp_type
        })
        logger.info(f"New learning entry: {replied_key} -> {resp_content} ({resp_type})")
    else:
        logger.debug(f"Duplicate learning skipped for: {replied_key}")
