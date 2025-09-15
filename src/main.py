import config
import client
import sys

    
if __name__ == "__main__":
    if not config.read_config():
        sys.exit() # Exit if config file was just created
    client.connect_to_Telegram()
    client.client.run_until_disconnected()
