import config
import client

    
if __name__ == "__main__":
    config.read_config()
    client.connect_to_Telegram()
    client.client.run_until_disconnected()
