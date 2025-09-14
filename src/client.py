from config import save_config
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, MessageMediaPhoto, MessageMediaWebPage, Photo, WebPage
from telethon.tl.patched import Message
from telethon.events import NewMessage


def connectToTelegram(config):
    client = TelegramClient("./data/bot", config.id, config.hash)
    client.connect()
    
    if client.is_user_authorized():
        client.user = client.get_me()
        print("Client sucessfully started. running with user: " + client.user.username)
        client.add_event_handler(handler, NewMessage())
        return client
    else:
        print("Failed to start the client. Sending code request...")
        client.send_code_request(config.phone)
        code = input("Enter the code you received: ")
        client.sign_in(config.phone, code)
        if client.is_user_authorized():
            client.user = client.get_me()
            print("Client sucessfully started. running with user: " + client.user.username)
            client.add_event_handler(handler, NewMessage())
            return client
        else:
            print("Failed to start the client. Please restart the program and try again.")
            return False
    

async def handler(message: Message):
    try:
        if message.chat.id == config.config_chat:
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
                    chat =f"CHAT NAME: {dialog.name}\nCHAT ID:{message.chat.id}"
                await message.reply(chat)
            
            elif message.text.startswith("addid"):
                id = int(message.text.split(" ")[1])
                if id not in (c["id"] for c in config.chats):
                    entity = await client.get_entity(id)
                    channel_name = entity.title if hasattr(entity, "title") else str(entity)
                    config.chats.append({"title": channel_name, "id": id})
                    save_config(config)
                    await message.reply(f"Successfully added the ID {id} ({channel_name}) to the monitored list!")
                else:
                    await message.reply("The ID is already being monitored.")
                    
            elif message.text.startswith("rmvid"):
                id = int(message.text.split(" ")[1])
                chat_to_remove = next((c for c in config.chats if c["id"] == id), None)
                if chat_to_remove:
                    config.chats.remove(chat_to_remove)
                    save_config(config)
                    await message.reply(f"Successfully removed '{chat_to_remove['title']}' with ID {id} from the monitored list!")
                else:
                    await message.reply("This ID is not being monitored.")
            elif message.text.startswith("listid"):
                a = "Monitored chats:\n"
                for chat in config.chats:
                    a += f"[{chat['title']}] - {id}"
                    if chat != config.chats[-1]:
                        a += "\n"
            await message.reply(a)
                    
        ############################################### DESATUALIZADO #####################################################
    
       
        
        elif message.chat.id in (chat.id for chat in config.chats):
            try:
                blocked_words = [
                    "PROMOBUGS50",
                ]
                for i in blocked_words: 
                    if i in message.text:
                        return



                splited = message.text.split("http")
                links = []
                del splited[0]
                for parte in splited:
                    og = ("http" + parte.split(" ")[0]).replace("\n","")
                    if "awin1.com" not in parte:
                        og = ("http" + parte.split(" ")[0]).replace("\n","")
                        ml = ("http" + parte.split(" ")[0]).replace("\n","").replace("%3A", ":").replace("%2F", "/")
                        links.append({"og": og, "ml": ml})
                substituir = []
                for link in links:
                    substituir.append(
                        {
                            "old":link["og"],
                            "new":link["ml"].split("?")[0] + (")" if link["ml"].endswith(")") else "")
                    }
                )
                # print(substituir)
                nova = deepcopy(message.text)
                for substuicao in substituir:
                    nova = nova.replace(substuicao["old"],"<" + substuicao["new"]+">")


                if "awin1.com" in nova:
                    sla = "http" + (nova.split("&ued=")[0] + "&ued=").split("http")[1]
                    nova = nova.replace(sla,"")

                if "https://gafanho.to/images/" in nova:
                    code = nova.split("https://gafanho.to/images/")[1].split("_")[0]
                    url_code = f"https://gafanho.to/images/{code}_telegram.png"
                    nova = nova.replace(url_code,"").replace("[",'').replace("]","").replace("<","").replace(">","").replace("()","") + "\n" + url_code



                preco = ""

                if len(preco) > 1:
                    preco = f'[{preco}] - '
                else:
                    matches = []
                    for line in nova.split("\n"):
                        rg = re.findall("\\d{1,}(?:[.,]\\d{3})*(?:[.,]\\d{1,3})", line)
                        #print(rg)
                        if not rg: continue
                        filtro_de = ["de:", "de r$", "antes r$", " pol"]
                        teve_de = False
                        for de in filtro_de:
                            if de in line.lower():
                                teve_de = True
                                break
                        if teve_de: continue
                        for rgd in rg:
                            if "." in rgd and "," in rgd:
                                matches.append(float(rgd.replace(".","").replace(",",".")))
                            else:
                                matches.append(float(rgd.replace(",",".")))
                    if matches:
                        preco = False#"[R${}] - ".format(str(max(matches)))

                treco = str("{}{}".format(preco if preco else '',nova) + "ㅤ")
                treco = treco.replace("<","").replace(">","").replace("ㅤ","").replace("ㅤ","").replace("%E3%85%A4","").replace("%e3%85%a4",'')
                payload_embed = {"content": "","embeds": [{"description": str(treco),"color": 15620644}],"username": "SLND Promos","avatar_url": "https://cdn.discordapp.com/avatars/881608187810291732/3f51999706c4212b89f779ae4c16a4ad.webp?size=160","attachments": []}
                print(treco)
                
                files = None
                # print(message.media)
                if message.media and type(message.media) == MessageMediaPhoto:
                    # print("would use")
                    await message.download_media(file="foto.jpg")
                    with open("foto.jpg", "rb") as f:
                        files = {"foto.jpg": f.read()}
            
                for url in config["webhooks"]:
                    if message.chat.id == 1403612364 and not str(url).startswith("https://discord.com/api/webhooks/999016935108923422/"):
                        continue
                        
                    if len(treco) > 3: 
                        r = requests.post(url, json=payload_embed)  # Só pra não enviar em branco
                        print("[PROMO] [{}] - [{}]".format(url,r.text))

                    if files:
                        r = requests.post(url, files=files, data={"username": "SLND Promos", "avatar_url": "https://cdn.discordapp.com/avatars/881608187810291732/3f51999706c4212b89f779ae4c16a4ad.webp?size=160"})
                    

                    # print(r.text)
            except:
                traceback.print_exc()
                pass
        else:
            pass    
    except:
        pass





if __name__ == "__main__":
    from config import read_config
    config = read_config()
    if not config:
        print("Please fill in the config.json file and restart the program.")
        exit(0)
    
    client = connectToTelegram(config.config)

        
        