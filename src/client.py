import config
from webhook import send_webhook
from telethon.sync import TelegramClient
from telethon.tl.patched import Message
from telethon.events import NewMessage

client = None

def connect_to_Telegram():
    global client
    client = TelegramClient("./data/bot", config.config.user_id, config.config.user_hash)
    client.connect()
    
    if client.is_user_authorized():
        client.user = client.get_me()
        print("Client sucessfully started. running with user: " + client.user.username)
        client.add_event_handler(handler, NewMessage())
        return client
    else:
        print("Failed to start the client. Sending code request...")
        client.send_code_request(config.config.phone)
        code = input("Enter the code you received: ")
        client.sign_in(config.config.phone, code)
        if client.is_user_authorized():
            client.user = client.get_me()
            print("Client sucessfully started. running with user: " + client.user.username)
            client.add_event_handler(handler, NewMessage())
            return client
        else:
            print("Failed to start the client. Please restart the program and try again.")
            return False
    

async def handler(message: Message):
    if message.chat_id == config.config.config_chat:
        # Commands to manage monitored chats
        if message.text.startswith("checkid"):
            if " " in message.text:
                query = message.text.split("checkid ")[1].lower()
                # fetch dialogs (limit optional, default fetches all)
                dialogs = await client.get_dialogs(limit=200)  # similar to your chunk_size
                # search for a group whose title matches the query
                for dialog in dialogs:
                    if dialog.is_group or dialog.is_channel:   # optional: only groups/channels
                        if dialog.name.lower() == query:
                            chat = f"CHAT NAME: {dialog.name}\nCHAT ID:{dialog.id}"
                            break
            else:
                # Get the id of the current chat
                chat =f"CHAT NAME: {message.chat.title}\nCHAT ID:{message.chat.id}"
            await message.reply(chat)
        
        elif message.text.startswith("addid"):
            id = int(message.text.split(" ")[1])
            if id not in (c["id"] for c in config.config.chats):
                entity = await client.get_entity(id)
                channel_name = entity.title if hasattr(entity, "title") else str(entity)
                config.config.chats.append({"title": channel_name, "id": id})
                config.save_config()
                await message.reply(f"Successfully added the ID {id} ({channel_name}) to the monitored list!")
            else:
                await message.reply("The ID is already being monitored.")
                
        elif message.text.startswith("rmvid"):
            id = int(message.text.split(" ")[1])
            chat_to_remove = next((c for c in config.config.chats if c["id"] == id), None)
            if chat_to_remove:
                config.config.chats.remove(chat_to_remove)
                config.save_config()
                await message.reply(f"Successfully removed '{chat_to_remove['title']}' with ID {id} from the monitored list!")
            else:
                await message.reply("This ID is not being monitored.")
        elif message.text.startswith("listids"):
            a = "Monitored chats:\n"
            for chat in config.config.chats:
                a += f"[{chat['title']}] - {id}"
                if chat != config.config.chats[-1]:
                    a += "\n"
            await message.reply(a)
                
    
    elif message.chat_id in (chat['id'] for chat in config.config.chats):
        # Message from monitored chat, forward to webhooks
        await send_webhook(message)
    
    else:
        # Message from unmonitored chat, ignore
        return


if __name__ == "__main__":
    config.read_config()
    if not config:
        print("Please fill in the config.json file and restart the program.")
        exit(0)
    
    connect_to_Telegram(config.config)

        
        