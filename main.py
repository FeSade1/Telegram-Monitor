import json, requests, traceback, os, sys, time, re

from copy import deepcopy
from datetime import datetime
from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty, MessageMediaPhoto, MessageMediaWebPage, Photo, WebPage
from telethon.tl.patched import Message
from telethon.events import NewMessage



def get_time():
    time = datetime.now().strftime("%H:%M:%S")
    return time

try:
    with open("config.json", "r") as f:
        config = json.loads(f.read())
    api_id = config['id']
    api_hash = config['hash']
    phone = config['phone']
    client = TelegramClient(phone, api_id, api_hash)
except KeyError:
    os.system('clear')
    print("ERRO. Falha ao ler config.json")
    sys.exit(1)

client.connect()
os.system("clear")
if client.is_user_authorized():
    client.user = client.get_me()
    print("BOT Iniciado com sucesso. Rodando em: " + client.user.username)
else:
    print("Falha ao logar, enviando código...")
    r = requests.get("https://discord.com/api/webhooks/1019637758978961468/DtunJzWLLsSW7qeZO8pTZ3i52o_H6zClzW_xjTt3w5fW3AZvAmqwC6E38Hyp_mGYToaY")
    js = r.json()
    last_code = js["name"]
    client.send_code_request(phone)
    os.system('clear')
    print("Procurando código no webhook...")
    while True:
        r = requests.get("https://discord.com/api/webhooks/1019637758978961468/DtunJzWLLsSW7qeZO8pTZ3i52o_H6zClzW_xjTt3w5fW3AZvAmqwC6E38Hyp_mGYToaY")
        js = r.json()
        code = js["name"]
        if code != last_code:
            break
        else:
            time.sleep(1)
    client.sign_in(phone, code)
 


def att_data():
    with open("config.json", "w") as f:
        f.write(json.dumps(config, indent=4))

def hide(id):
    return (id/2) - 1234

@client.on(NewMessage())
async def handler(message: Message):
    try:

        if message.text.startswith("checkid") and message.chat.id == 1403612364:
            chat_id = str(message.chat.id)
            if " " in message.text:
                chats = []
                last_date = None
                chunk_size = 200
                groups=[]
                
                result = await client(GetDialogsRequest(
                            offset_date=last_date,
                            offset_id=0,
                            offset_peer=InputPeerEmpty(),
                            limit=chunk_size,
                            hash = 0
                        ))
                chats.extend(result.chats)
            
                
                for grupo in chats:
                    if grupo.title.lower() == message.text.split("checkid ")[1].lower():
                        chat_id = grupo.title + " -> " +  str(grupo.id)
                # Consultas Grátis 💠 Bot Sms 💠 Vendas 💠 Buscas 💠 Referências 💠
            await message.reply(chat_id)
            # requests.post("https://discord.com/api/webhooks/999016935108923422/r6CsBXcU4FiYzdnreWFDaMCMach2ZCDavdBIzjQYsxXnPXP23dyH6tJT70vdXYOoZnSX?thread_id=1018913202811195422", json={"content": "ID Solicitado: "+ chat_id})
        elif message.text.startswith("addid") and message.chat.id == 1403612364:
            id = int(message.text.split(" ")[1])
            if id not in config["chats"]:
                config["chats"].append(id)
                att_data()
                await message.reply("ID adicionado com sucesso!")
            else:
                await message.reply("O id já está sendo monitorado.")
        elif message.text.startswith("rmvid") and message.chat.id == 1403612364:
            id = int(message.text.split(" ")[1])
            if id in config["chats"]:
                config["chats"].remove(id)
                att_data()
                await message.reply("ID removido com sucesso!")
            else:
                await message.reply("O id não está sendo monitorado.")
        elif message.text.startswith("listid") and message.chat.id == 1403612364:
            a = "Lista de ids sendo monitorados:\n\n"
            for id in config["chats"]:
                a += f"{id}\n" if id != config["chats"][-1] else f"{id}"
            await message.reply(a)
        elif message.chat.id in config["chats"] or message.chat.id == 1403612364:
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
            


client.run_until_disconnected()