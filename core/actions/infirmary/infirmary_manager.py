# core/actions/infirmary/infirmary_manager.py
from core.actions.base.interaction import Interaction
from core.state.state_bot import BotState
from core.state.state_analyzer import StateAnalyzer

from utils.constants import CONST
from utils import assets_repository
from utils.log import warning, info, debug, error
from utils.helper import sleep


class InfirmaryManager:
    def __init__(self, interaction: Interaction, state_analyzer: StateAnalyzer):
        self.interaction = interaction
        self.state_analyzer = state_analyzer
        self.skipped_infirmary = False

    def handle_infirmary_decision(self, state: BotState, matches, screen) -> bool:
        if not matches.get("infirmary"):
            return False

        infirmary_btn = matches["infirmary"][0]
        if not self.interaction.recognizer.is_btn_active(
            region=infirmary_btn, screen=screen
        ):
            return False

        if state.should_visit_infirmary:
            self.visit_infirmary()
            return True
        else:
            info("Skipping infirmary because of high energy.")
            self.skipped_infirmary = True
            return False

    def _has_severe_conditions(self) -> bool:
        """Check if has severe conditions that require infirmary"""
        info("Since we skipped infirmary, check full stats for severe conditions.")
        if not self.interaction.click_element(
            assets_repository.get_button("full_stats"), max_search_time=1
        ):
            warning("Couldn't find full stats button.")
            return False

        sleep(0.5)
        check_status_screen = self.interaction.input.take_screenshot(
            CONST.FULL_STATS_STATUS_REGION
        )
        sleep(0.5)

        conditions, total_severity = self.state_analyzer._check_status_effects(
            check_status_screen
        )

        self.interaction.click_element(
            assets_repository.get_button("close_btn"), max_search_time=1
        )

        return total_severity > 1

    def should_force_infirmary_after_skip(self) -> bool:
        """Check if should force infirmary after previously skipping"""
        return self.skipped_infirmary and self._has_severe_conditions()

    def visit_infirmary(self) -> bool:
        """Forcing to visit infirmary"""
        self.skipped_infirmary = False
        self.interaction.click_element(
            assets_repository.get_button("infirmary_btn"), max_search_time=2
        )
