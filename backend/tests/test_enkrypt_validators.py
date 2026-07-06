"""
Mentra X — Unit & Integration Tests for Milestone 7.1 (Enkrypt Safety Layer Foundation)
Tests the 4 validation pipelines, weighted confidence scoring, and decision thresholds.
"""

import pytest
import time
from backend.services.enkrypt.math_validator import MathValidator
from backend.services.enkrypt.science_validator import ScienceFactValidator
from backend.services.enkrypt.hallucination_detector import HallucinationDetector
from backend.services.enkrypt.pedagogy_evaluator import PedagogyEvaluator
from backend.services.enkrypt.enkrypt_validator import EnkryptValidator


class TestMathValidator:
    def setup_method(self):
        self.validator = MathValidator()

    def test_valid_formula(self):
        score, flags = self.validator.validate("In Einstein's relativity, E = m*c^2 is valid.", exam_track="JEE")
        assert score == 1.0
        assert len(flags) == 0

    def test_delta_s_misapplication(self):
        # Using dS = Q/T without reversible or isothermal context
        score, flags = self.validator.validate("To find entropy change in this general process, use dS = Q/T directly.", exam_track="JEE")
        assert score <= 0.50
        assert any("misapplied" in f for f in flags)

    def test_incorrect_force_formula(self):
        score, flags = self.validator.validate("Force is calculated as F = m*v in Newton's mechanics.", exam_track="NEET")
        assert score <= 0.50
        assert any("F = m*v" in f for f in flags)


class TestScienceFactValidator:
    def setup_method(self):
        self.validator = ScienceFactValidator()

    def test_entropy_contradiction(self):
        score, flags = self.validator.validate("As we know, entropy always increases in reversible adiabatic cycles.", subject_tag="physics")
        assert score <= 0.40
        assert any("contradiction" in f.lower() for f in flags)

    def test_mitochondria_error(self):
        score, flags = self.validator.validate("During photosynthesis, mitochondria synthesize glucose.", subject_tag="biology")
        assert score <= 0.40
        assert any("mitochondria" in f.lower() for f in flags)


class TestHallucinationDetector:
    def setup_method(self):
        self.validator = HallucinationDetector()

    def test_fabricated_theorem(self):
        score, flags = self.validator.validate("According to Newton's fourth law of thermodynamics, heat flows upwards.", "physics")
        assert score <= 0.30
        assert any("Fabrication detected" in f for f in flags)


class TestEnkryptValidator:
    def setup_method(self):
        self.validator = EnkryptValidator()

    def test_approve_threshold(self):
        start = time.time()
        res = self.validator.validate(
            text="In classical mechanics, Newton's second law states that F = m*a. Let's solve this step-by-step: 1) identify mass, 2) multiply by acceleration.",
            subject_tag="physics",
            exam_track="JEE",
            level=2
        )
        latency_ms = (time.time() - start) * 1000.0
        assert latency_ms < 500.0
        assert res.composite_confidence >= 0.90
        assert res.recommended_action == "APPROVE"

    def test_regenerate_threshold(self):
        # A response with a unit inconsistency that drops confidence between 0.70 and 0.90
        res = self.validator.validate(
            text="The car travels at 50 km/h and accelerates at 2 m/s directly.",
            subject_tag="physics",
            exam_track="JEE",
            level=1
        )
        assert 0.70 <= res.composite_confidence < 0.90
        assert res.recommended_action == "REGENERATE"
        assert len(res.flagged_claims) > 0

    def test_hard_fail_threshold(self):
        # A response with multiple hallucinations and formula errors
        res = self.validator.validate(
            text="According to Newton's fourth law, entropy always increases in reversible cycles and F = m*v.",
            subject_tag="physics",
            exam_track="JEE",
            level=1
        )
        assert res.composite_confidence < 0.70
        assert res.recommended_action == "HARD_FAIL"
        assert len(res.flagged_claims) >= 2
