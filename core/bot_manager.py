import core.config as config
from core.bot import Bot
from utils.log import info, debug, error
from utils.adb_helper import ADB
import threading


class BotManager:
    def __init__(self, adb: ADB):
        self.adb = adb
        self.bot = None
        self.bot_thread = None
        self.is_running = False

    def start(self):
        """Start or restart the bot with current config"""
        if self.is_running:
            self.stop()

        config.reload_config()

        self._update_global_constants()

        if self.bot is None:
            # Create new bot instance
            self.bot = Bot(self.adb, scenario=config.SCENARIO)
            debug("New bot instance created")
        else:
            # Update existing bot with new scenario if changed
            if self.bot.scenario != config.SCENARIO:
                self.bot.update_scenario(config.SCENARIO)

        # Start the bot
        self.bot.start()
        self.bot_thread = threading.Thread(target=self.bot.run, daemon=True)
        self.bot_thread.start()
        self.is_running = True

    def stop(self):
        """Stop the bot"""
        if self.bot and self.bot.is_running:
            self.bot.stop()
            self.is_running = False

    def restart(self):
        """Restart the bot"""
        info("Restarting bot...")
        self.stop()
        self.start()

    def get_status(self):
        """Get current bot status"""
        return {
            "is_running": self.is_running,
            "scenario": self.bot.scenario if self.bot else None,
            "config_name": config.CONFIG_NAME,
        }

    def _update_global_constants(self):
        """Update global CONST based on current scenario"""
        import utils.constants as constants

        constants.ACTIVE_SCENARIO = config.SCENARIO
        debug(f"Global CONST updated to scenario: {config.SCENARIO}")
