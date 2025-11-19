import core.config as config
from core.state.state_analyzer import BotState
from core.actions.training.training_manager import TrainingManager
from utils.log import info, debug
from utils.helper import sleep


class BaseFlow:
    def __init__(self):
        self.training = None

    def handle_race_day(self, state: BotState):
        """Handle race day logic"""
        info("Race day.")

        if state.is_buy_skill:
            self.skill.buying_skills()

        sleep(0.5)
        self.race.handle_race_day(is_finale=False)

    def handle_ura_finale(self, state: BotState):
        """Handle race day logic"""
        info("Race day.")

        if state.is_buy_skill:
            self.skill.buying_skills()

        sleep(0.5)
        self.race.handle_race_day(is_finale=True)

    def handle_g1_race(self, state: BotState) -> bool:
        """Handle G1 race priority"""
        race_done = False
        for race_list in config.RACE_SCHEDULE:
            if len(race_list):
                if race_list["year"] in state.year and race_list["date"] in state.year:
                    debug(
                        f"Race now, {race_list['name']}, {race_list['year']} {race_list['date']}"
                    )
                    if self.race.handle_g1_race(race_list["name"]):
                        race_done = True
                        break
        return race_done

    def handle_goal_race(self) -> bool:
        """Handle goal-based race"""
        race_found = self.race.handle_goal_race()
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
