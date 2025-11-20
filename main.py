import threading
import keyboard
import uvicorn
import traceback

from utils.helper import sleep
from utils.log import info, error

from core.bot_manager import BotManager

from update_config import update_config
from server.main import app

hotkey = "f1"
bot_manager = BotManager()


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
    bot_manager.connect_adb()
    start_server()
