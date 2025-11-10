import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Telegram API credentials
API_ID = int(os.getenv("API_ID")) if os.getenv("API_ID") else None
API_HASH = os.getenv("API_HASH", None)
GPT_API = os.getenv("GPT_API")

# Bot token and MongoDB URL fetched from environment variables
BOT_TOKEN = os.getenv("BOT_TOKEN", None)
MONGO_URL = os.getenv("MONGO_URL", None)
RAPIDAPI_KEY = os.getenv("RAPIDAPI_KEY")

# Bot owner's Telegram user ID and username
OWNER_ID = int(os.getenv("OWNER_ID")) if os.getenv("OWNER_ID") else 8088623806
OWNER_USERNAME = "EliteSid"

# Support group and update channel names
SUPPORT_GROUP = "VivaanSupport"
UPDATE_CHANNEL = "VivaanNetwork"
