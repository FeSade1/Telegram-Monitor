import os, json
from types import SimpleNamespace


def save_config(config):
    with open("./data/config.json", "w", encoding='utf-8') as f:
        f.write(json.dumps(config, indent=4, ensure_ascii=False))
        
        
def read_config():
    if not os.path.exists("./data/config.json"):
        with open("./data/config.json", 'w') as f:
            f.write(json.dumps(
                                {
                                    "user_id": "YOUR_TELEGRAM_ID",
                                    "user_hash": "YOUR_TELEGRAM_HASH",
                                    "user_phone": "YOUR_TELEGRAM_PHONE_NUMBER",
                                    "config_chat": 0,
                                    "chats": [],
                                    "webhooks": []
                                }, 
                                indent=4
                            )
                    )
            print("config.json file created.")
            return False
    else:
        with open("./data/config.json", 'r') as f:
            config = json.loads(f.read())
            return SimpleNamespace(**config)
        

        
        
        
if __name__ == "__main__":
    print(read_config())