from dotenv import load_dotenv
import os
from telethon import TelegramClient
from telethon.tl.types import MessageMediaPhoto
import pandas as pd
from tqdm import tqdm

# Load credentials
load_dotenv()
api_id = int(os.getenv("API_ID"))
api_hash = os.getenv("API_HASH")
session_name = os.getenv("SESSION_NAME")

# Initialize client
client = TelegramClient(session_name, api_id, api_hash)

# Set target channel
channel_username = "@Leyueqa"
output_dir = f"data/{channel_username.strip('@').lower()}"
media_dir = f"{output_dir}/media"
os.makedirs(media_dir, exist_ok=True)

# Main async block
async def main():
    await client.start()
    messages = []

    all_msgs=[]
    async for msg in client.iter_messages(channel_username, limit=200):
        all_msgs.append(msg)

        for msg in tqdm(all_msgs):
            if not msg.message:
                continue

        row = {
            "channel": channel_username,
            "message_id": msg.id,
            "date": msg.date.strftime('%Y-%m-%d %H:%M:%S'),
            "sender_id": msg.sender_id,
            "text": msg.message.strip(),
            "has_media": False,
            "media_file": None
        }

        # Download image if available
        if isinstance(msg.media, MessageMediaPhoto):
            row["has_media"] = True
            file_name = f"{media_dir}/{msg.id}.jpg"
            try:
                await client.download_media(msg, file=file_name)
                row["media_file"] = file_name
            except Exception as e:
                print(f"⚠️ Failed to download media: {e}")

        messages.append(row)

    # Save CSV
    df = pd.DataFrame(messages)
    df.to_csv(f"{output_dir}/messages.csv", index=False, encoding="utf-8-sig")
    print(f"\n Saved {len(df)} messages to {output_dir}/messages.csv")

# Run it
with client:
    client.loop.run_until_complete(main())

