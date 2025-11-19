# core/state/create_analyzer.py
from .state_analyzer import URAStateAnalyzer, UnityCupStateAnalyzer
from core.ocr import OCR
from core.recognizer import Recognizer
from utils.log import debug, error


def create_state_analyzer(scenario: str, ocr: OCR, recognizer: Recognizer):
    scenario = scenario.lower()
    debug(f"Create state analyzer for scenario: {scenario}")
    if scenario == "ura":
        analyzer = URAStateAnalyzer(ocr, recognizer)
    elif scenario == "unity":
        analyzer = UnityCupStateAnalyzer(ocr, recognizer)
    else:
        error(f"Unkown scenario: {scenario}")
        return None

    debug(
        f"State analyzer created: {analyzer is not None}, type: {type(analyzer).__name__}"
    )
    return analyzer
