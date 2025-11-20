import core.config as config
from core.bot import Bot
from utils.log import info, debug, error
from utils.adb_helper import ADB
import threading


class BotManager:
    def __init__(self):
        self.adb = ADB("127.0.0.1:5557")
        self.bot = None
        self.bot_thread = None
        self.is_running = False
        self._is_connected = False

    def connect_adb(self):
        """Connect to ADB"""
        self.adb.connect()
        self._is_connected = True

    def start(self):
        """Start bot - always create NEW instance"""
        if self.is_running:
            self.stop()

        config.reload_config()

        if not self._is_connected:
            self.connect_adb()

        # Create new instance
        self.bot = Bot(self.adb, scenario=config.SCENARIO)
        debug("New bot instance created")

        # Start the bot
        self.bot.start()
        self.bot_thread = threading.Thread(target=self.bot.run, daemon=True)
        self.bot_thread.start()
        self.is_running = True

    def stop(self):
        """Stop bot and DESTROY instance"""
        if self.bot and self.bot.is_running:
            self.bot.stop()

        # DESTROY BOT INSTANCE
        self.bot = None
        self.bot_thread = None
        self.is_running = False
        debug("Bot instance destroyed")

    def get_status(self):
        """Get current bot status"""
        return {
            "is_running": self.is_running,
            "scenario": self.bot.scenario if self.bot else None,
            "config_name": config.CONFIG_NAME,
        }
