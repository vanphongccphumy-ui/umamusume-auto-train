# core/actions/training/training_manager.py
from .support_analyzer import SupportAnalyzer
from .training_strategy import TrainingStrategy

from core.actions.base import Interaction
from core.state.state_analyzer import StateAnalyzer

from utils.log import info
from utils.assets_repository import get_icon
from utils.constants import CONST


class TrainingManager:
    def __init__(
        self,
        interaction: Interaction,
        state_analyzer: StateAnalyzer,
        energy_level,
        current_stats,
    ):
        self.interaction = interaction
        self.energy_level = energy_level
        self.current_stats = current_stats

        self.analyzer = SupportAnalyzer(interaction, state_analyzer)
        self.strategy = TrainingStrategy()

    def do_train(self, year):
        """Main training execution"""
        # Analyze training options
        training_data = self.analyzer.check_training()
        if not training_data:
            info("No training options found")
            return False

        # Select best training
        best_training = self.strategy.select_training(
            training_data, self.current_stats, self.energy_level, year
        )
        if not best_training:
            info("No suitable training found")
            return False

        # Execute training
        return self._execute_training(best_training)

    def _execute_training(self, training_type):
        """Execute the selected training"""
        x, y = CONST.TRAINING_ICON_COORD[training_type]
        if self.interaction.click_coordinates(x, y, clicks=3):
            return True
        # if self.interaction.click_element(get_icon(f"train_{training_type}"), clicks=3):
        #     return True
        return False
