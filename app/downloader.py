from telethon.sync import TelegramClient
import re

def fetch_telegraph_links(api_id, api_hash, channel_username):
    client = TelegramClient('session_name', api_id, api_hash)
    client.start()

    links = []
    for message in client.iter_messages(channel_username):
        if message.entities:
            for entity in message.entities:
                if hasattr(entity, 'url') and entity.url and 'telegra.ph' in entity.url:
                    links.append(entity.url)
        elif message.message:
            match = re.search(r'https://telegra\.ph/\S+', message.message)
            if match:
                links.append(match.group(0))
    client.disconnect()
    return links
