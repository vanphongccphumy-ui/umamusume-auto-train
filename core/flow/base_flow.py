# core/flow/base_flow.py
import core.config as config
from core.actions.base import Interaction, Input, Navigation
from core.actions import (
    InfirmaryManager,
    SkillManager,
    RaceManager,
    EventManager,
)
from core.ocr import OCR
from core.recognizer import Recognizer
from core.state.state_analyzer import StateAnalyzer
from utils.adb_helper import ADB
from core.actions.training.training_manager import TrainingManager
from core.state.state_bot import BotState
from utils.log import info, debug
from utils.helper import sleep


class BaseFlow:
    def __init__(
        self,
        adb: ADB,
        ocr: OCR,
        recognizer: Recognizer,
        state_analyzer: StateAnalyzer,
        input: Input,
        interaction: Interaction,
        navigation: Navigation,
        skill_manager: SkillManager,
        infirmary_manager: InfirmaryManager,
        event_manager: EventManager,
        race_manager: RaceManager,
    ):
        self.adb = adb
        self.ocr = ocr
        self.recognizer = recognizer
        self.state_analyzer = state_analyzer
        self.input = input
        self.interaction = interaction
        self.navigation = navigation
        self.skill_manager = skill_manager
        self.infirmary_manager = infirmary_manager
        self.event_manager = event_manager
        self.race_manager = race_manager
        self.training = None

    def handle_race_day(self, state: BotState):
        """Handle race day logic"""
        info("Race day.")

        if state.is_buy_skill:
            self.skill_manager.buying_skills()

        sleep(0.5)
        self.race_manager.handle_race_day(is_finale=False)

    def handle_ura_finale(self, state: BotState):
        """Handle race day logic"""
        info("Race day.")

        if state.is_buy_skill:
            self.skill_manager.buying_skills()

        sleep(0.5)
        self.race_manager.handle_race_day(is_finale=True)

    def handle_g1_race(self, state: BotState) -> bool:
        """Handle G1 race priority"""
        race_done = False
        for race_list in config.RACE_SCHEDULE:
            if len(race_list):
                if race_list["year"] in state.year and race_list["date"] in state.year:
                    debug(
                        f"Race now, {race_list['name']}, {race_list['year']} {race_list['date']}"
                    )
                    if self.race_manager.handle_g1_race(race_list["name"]):
                        race_done = True
                        break
        return race_done

    def handle_goal_race(self) -> bool:
        """Handle goal-based race"""
        race_found = self.race_manager.handle_goal_race()
        if race_found:
            return True
        else:
            sleep(0.5)
            return False

    def handle_training(self, state: BotState):
        """Handle training flow"""
        if not self.navigation.go_to_training():
            info("Training button not found.")
            return

        sleep(0.5)

        self.training = TrainingManager(
            self.interaction,
            self.state_analyzer,
            state.energy_level,
            state.current_stats,
        )

        if self.training.do_train(state.year):
            return
        else:
            self.navigation.go_back()
            sleep(0.5)
            if state.never_rest:
                info(f"Energy above {config.NEVER_REST_ENERGY}, skipping rest")
                return

            self.navigation.do_rest(state.is_summer)
