# core/flow/flow_manager.py
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
from utils.log import info, debug, error

from core.flow.scenario import URAFlow, UnityFlow


class FlowManager:
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
        self.training = None
        self.deps = {
            "adb": adb,
            "ocr": ocr,
            "recognizer": recognizer,
            "state_analyzer": state_analyzer,
            "input": input,
            "interaction": interaction,
            "navigation": navigation,
            "skill_manager": skill_manager,
            "infirmary_manager": infirmary_manager,
            "event_manager": event_manager,
            "race_manager": race_manager,
        }

        self.flows = {"ura": URAFlow(**self.deps), "unity": UnityFlow(**self.deps)}
        self.active_flow = None

    def activate(self, scenario):
        if scenario in self.flows:
            self.active_flow = self.flows[scenario]
            info(f"Run {scenario}")
        else:
            error(f"Invalid scenario: {scenario}")

    def run(self, screen, matches):
        if not self.active_flow:
            return
        self.active_flow.run(screen, matches)
