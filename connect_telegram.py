# 1. Load your environment variables securely
from dotenv import load_dotenv
import os

# 2. Import Telethon and connect
from telethon import TelegramClient

# 3. Load API credentials
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")

# 4. Initialize the client
client = TelegramClient(session_name, api_id, api_hash)

# 5. Start the session and test the connection
async def main():
    await client.start()
    me = await client.get_me()
    print(f"✅ Logged in as: {me.first_name} (@{me.username})")

with client:
    client.loop.run_until_complete(main())
