import threading
import keyboard
import uvicorn
import traceback

from utils.helper import sleep
from utils.log import info, error
from utils.adb_helper import ADB

import core.config as config

from core.bot_manager import BotManager

from update_config import update_config
from server.main import app

hotkey = "f1"
adb = ADB("127.0.0.1:5557")
bot_manager = BotManager(adb)


def main():
    print("Uma Auto!")
    try:
        config.reload_config()

        info(f"Config: {config.CONFIG_NAME}")
        bot_manager.start()
        threading.Thread(target=bot_manager.run, daemon=True).start()
    except Exception as e:
        error(f"Error in main thread: {e}")
        traceback.print_exc()


def toggle_bot():
    """Toggle bot start/stop"""
    if bot_manager.is_running:
        bot_manager.stop()
    else:
        try:
            bot_manager.start()
        except Exception as e:
            error(f"Failed to start bot: {e}")
            traceback.print_exc()


def hotkey_listener():
    while True:
        keyboard.wait(hotkey)
        toggle_bot()
        sleep(0.5)


def start_server():
    host = "127.0.0.1"
    port = 8000
    info(f"Press '{hotkey}' to start/stop the bot.")
    print(f"[SERVER] Open http://{host}:{port} to configure the bot.")
    config = uvicorn.Config(app, host=host, port=port, workers=1, log_level="warning")
    server = uvicorn.Server(config)
    server.run()


if __name__ == "__main__":
    update_config()
    threading.Thread(target=hotkey_listener, daemon=True).start()
    adb.connect()
    start_server()
