import requests, io, json
from telethon.tl.patched import Message
from telethon.tl.types import MessageMediaPhoto
import config


async def send_webhook(message: Message):
    # Base embed
    payload_embed = {
        "content": None,
        "embeds": [
            {
                "title": message.chat.title,
                "description": message.text,
                "color": 3187967,
                "author": {"name": ""},
            }
        ],
        "username": "SADE.AIO Telegram Monitor",
        "attachments": []
    }

    files = None
    data = {"payload_json": json.dumps(payload_embed)}

    if message.media and isinstance(message.media, MessageMediaPhoto):
        img_bytes = io.BytesIO()
        await message.download_media(file=img_bytes)
        img_bytes.seek(0)

        # Add file to upload
        files = {"file": ("foto.jpg", img_bytes, "image/jpeg")}

        # Reference uploaded file in embed image
        payload_embed["embeds"][0]["image"] = {"url": "attachment://foto.jpg"}

        # Update data (must re-dump JSON after modifying embed)
        data = {"payload_json": json.dumps(payload_embed)}

    for url in config.config.webhooks:
        if len(message.text) > 3 or files:
            if files:
                r = requests.post(url, data=data, files=files)
            else:
                r = requests.post(url, json=payload_embed)
