"""
Mentra X — Enkrypt AI Safety Layer Package (Phase 7 Layer 6)

Contains:
- Four-validator pipeline (MathValidator, ScienceFactValidator, HallucinationDetector, PedagogyEvaluator)
- Main Enkrypt orchestration & confidence scoring (EnkryptValidator)
- Regeneration loop & textbook fallback content service (RegenerationLoop, TextbookFallbackService)
- Safety monitoring & audit logging (SafetyMonitor)
"""

from .dto import ValidationResultDTO, FallbackContentDTO, RegenerationResultDTO
from .math_validator import MathValidator
from .science_validator import ScienceFactValidator
from .hallucination_detector import HallucinationDetector
from .pedagogy_evaluator import PedagogyEvaluator
from .enkrypt_validator import EnkryptValidator
from .textbook_fallback import TextbookFallbackService
from .regeneration_loop import RegenerationLoop
from .safety_monitor import SafetyMonitor, safety_monitor

__all__ = [
    "ValidationResultDTO",
    "FallbackContentDTO",
    "RegenerationResultDTO",
    "MathValidator",
    "ScienceFactValidator",
    "HallucinationDetector",
    "PedagogyEvaluator",
    "EnkryptValidator",
    "TextbookFallbackService",
    "RegenerationLoop",
    "SafetyMonitor",
    "safety_monitor"
]
