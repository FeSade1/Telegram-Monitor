# 📡 Telegram  Monitor

![Python](https://img.shields.io/badge/Python-3.9%2B-blue?logo=python)
![Telethon](https://img.shields.io/badge/Telethon-API-green)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)
![Discord](https://img.shields.io/badge/Discord-Webhook-blueviolet?logo=discord)

A simple Python bot that monitors Telegram chats/channels and forwards messages (including images) to one or more Discord webhooks.  
Built with [Telethon](https://github.com/LonamiWebs/Telethon).

---

## ✨ Features

- 🔍 Monitor multiple Telegram chats/channels by ID.  
- ⚡ Add/remove chats dynamically with Telegram commands:
  - `checkid` → check chat ID  
  - `addid <id>` → add chat to monitor list  
  - `rmvid <id>` → remove chat from list  
  - `listids` → list monitored chats  
- 📷 Forward messages with embedded images directly to Discord.  
- 🔧 Easy config file (`data/config.json`) to manage credentials & webhooks.  
- 💾 Persistent monitored chats list.  

---

## 📂 Project Structure

```
.
├── src/
│   ├── client.py      # Telegram client & event handlers
│   ├── config.py      # Config manager (JSON <-> SimpleNamespace)
│   ├── webhook.py     # Sends embeds/files to Discord
│   └── main.py        # Entry point
├── data/
│   └── config.json    # Created on first run
├── requirements.txt
├── README.md
└── LICENSE
```

---

## ⚙️ Installation

1. Clone the repo:
   ```bash
   git clone https://github.com/yourusername/telegram-discord-monitor.git
   cd telegram-discord-monitor
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Run once to generate the `data/config.json` file:
   ```bash
   python src/main.py
   ```

4. Edit `data/config.json` with your [Telegram API credentials](https://my.telegram.org) and Discord webhooks.

---

## 📜 Example `config.json`

```json
{
  "user_id": "YOUR_TELEGRAM_ID",
  "user_hash": "YOUR_TELEGRAM_HASH",
  "user_phone": "YOUR_PHONE",
  "config_chat": 123456789,
  "chats": [],
  "webhooks": [
    "https://discord.com/api/webhooks/123/xxx"
  ]
}
```

---

## ▶️ Usage

Start the bot:
```bash
python src/main.py
```

From your `config_chat` (the control chat you set in config), you can now use commands like:

```
checkid
addid 123456789
rmvid 123456789
listids
```

Messages from monitored chats will be forwarded to your Discord webhooks automatically. 🎉

---

## 🛠️ Requirements

- Python 3.9+  
- [Telethon](https://github.com/LonamiWebs/Telethon)  
- requests  

(see `requirements.txt` for exact versions)

---

## 🤝 Contributing

Pull requests and feature requests are welcome!  
For major changes, please open an issue first to discuss what you’d like to change.

---

## 📜 License

MIT License — feel free to use and adapt.
