from os import getenv
from dotenv import load_dotenv

load_dotenv()

API_ID = int(getenv("API_ID"))
API_HASH = getenv("API_HASH")
BOT_TOKEN = getenv("BOT_TOKEN")

OWNER_ID = int(getenv("OWNER_ID", "5451878368"))
OWNER_NAME = getenv("OWNER_NAME", "ᯓ 𓆩 ˹𝙱𝙴𝙽˼ 𓆪 #1")

SUBSCRIBE_CHANNEL = getenv("SUBSCRIBE_CHANNEL", "BENfiles")

