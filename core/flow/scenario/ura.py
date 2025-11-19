# core/flow/scenario/ura.py
from core.flow.base_flow import BaseFlow
from utils.log import info, debug


class URAFlow(BaseFlow):
    def __init__(self, **deps):
        super().__init__(**deps)

    def run(self, screen, matches):
        # 3. analyze state
        state = self.state_analyzer.analyze_current_state(screen)

        info("Checking state")

        # 4. Print state info
        print(
            "\n=======================================================================================\n"
        )
        info(f"Year: {state.year}")
        info(f"Mood: {state.mood}")
        info(f"Turn: {state.turn}")
        info(f"Energy: {state.energy_level:.2f}")
        info(f"Criteria: {state.criteria}")
        if state.is_race_day:
            info(f"Skill pts: {state.skill_pts}")
        else:
            info(f"Stat: {state.current_stats}")
        print(
            "\n=======================================================================================\n"
        )

        # 5. Main game logic
        if state.is_race_day:
            if "Finale" in state.year:
                debug("URA Finale!!!!")
                self.handle_ura_finale(state)
                return
            else:
                debug("Race Day!!!!")
                self.handle_race_day(state)
                return

        if state.should_prioritize_g1:
            debug("Race schedule!")
            if self.handle_g1_race(state):
                return

        if state.should_race_for_goals:
            debug("Race Goal!!")
            if self.handle_goal_race():
                return

        if self.infirmary_manager.handle_infirmary_decision(state, matches, screen):
            debug("Infirmary!")
            return
        if state.needs_increase_mood:
            if self.infirmary_manager.should_force_infirmary_after_skip():
                info(
                    "Severe condition found, visiting infirmary even though we will waste some energy."
                )
                self.infirmary_manager.visit_infirmary()
                return
            info("Mood is low, trying recreation to increase mood")
            self.navigation.do_recreation(state.is_summer)
            return

        debug("handle_training")
        self.handle_training(state)
