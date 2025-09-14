from config import read_config
from client import connectToTelegram

    
if __name__ == "__main__":
    config = read_config()
    client = connectToTelegram(config)
    client.run_until_disconnected()
