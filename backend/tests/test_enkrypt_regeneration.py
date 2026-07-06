"""
Mentra X — Unit & Integration Tests for Milestone 7.2 (Regeneration Loop & Textbook Fallback Service)
Tests textbook content retrieval, up-to-2-attempt revision loops, and double-failure HITL fallback triggering.
"""

import pytest
from backend.services.enkrypt.textbook_fallback import TextbookFallbackService
from backend.services.enkrypt.regeneration_loop import RegenerationLoop
from backend.services.enkrypt.enkrypt_validator import EnkryptValidator


class TestTextbookFallbackService:
    def setup_method(self):
        self.service = TextbookFallbackService()

    def test_seeded_fallback_retrieval(self):
        fb_jee = self.service.get_fallback("thermodynamics", exam_track="JEE", subject="physics")
        assert "Second Law" in fb_jee.content_text
        assert "NCERT" in fb_jee.source
        assert fb_jee.exam_track == "JEE"

        fb_neet = self.service.get_fallback("photosynthesis", exam_track="NEET", subject="biology")
        assert "chloroplasts" in fb_neet.content_text
        assert "NCERT" in fb_neet.source

    def test_unseeded_fallback_retrieval(self):
        fb_gen = self.service.get_fallback("string_theory", exam_track="JEE", subject="physics")
        assert "Standard Reference Content" in fb_gen.content_text
        assert "Official JEE Standard Reference" in fb_gen.source


class TestRegenerationLoop:
    def setup_method(self):
        self.loop = RegenerationLoop()
        self.validator = EnkryptValidator()

    def test_approve_no_regeneration(self):
        original = "In classical mechanics, E = m*c^2 is Einstein's mass-energy formula."
        initial_val = self.validator.validate(original, subject_tag="physics", exam_track="JEE")
        assert initial_val.recommended_action == "APPROVE"

        res = self.loop.execute(
            original_output=original,
            initial_validation=initial_val,
            tutor_generator_fn=lambda prompt: "Should not be called",
            concept="relativity",
            exam_track="JEE"
        )
        assert res.attempts_used == 0
        assert res.was_fallback_served is False
        assert res.hitl_flagged is False
        assert res.final_output == original

    def test_successful_regeneration_attempt_1(self):
        original = "The car travels at 50 km/h and accelerates at 2 m/s directly without converting units."
        initial_val = self.validator.validate(original, subject_tag="physics", exam_track="JEE")
        assert initial_val.recommended_action == "REGENERATE"

        # Mock generator returning a corrected string on attempt 1
        def mock_generator(instruction):
            assert "Previous response failed" in instruction
            return "To solve this, first convert speed from km/h to m/s by multiplying by 5/18, then apply acceleration."

        res = self.loop.execute(
            original_output=original,
            initial_validation=initial_val,
            tutor_generator_fn=mock_generator,
            concept="kinematics",
            exam_track="JEE"
        )
        assert res.attempts_used == 1
        assert res.was_fallback_served is False
        assert res.hitl_flagged is False
        assert "Enkrypt Verified after refinement" in res.final_output
        assert res.validation_result.composite_confidence >= 0.90

    def test_double_failure_fallback_and_hitl(self):
        original = "According to Newton's fourth law of thermodynamics, entropy always increases in reversible cycles and F = m*v."
        initial_val = self.validator.validate(original, subject_tag="physics", exam_track="JEE")
        assert initial_val.recommended_action == "HARD_FAIL"

        # Mock generator returning hallucinated or wrong formulas for both attempts
        def mock_generator_bad(instruction):
            return "According to Newton's fourth law, entropy always increases in reversible cycles."

        res = self.loop.execute(
            original_output=original,
            initial_validation=initial_val,
            tutor_generator_fn=mock_generator_bad,
            concept="thermodynamics",
            exam_track="JEE"
        )
        assert res.attempts_used == 2
        assert res.was_fallback_served is True
        assert res.hitl_flagged is True
        assert "NCERT Physics Class XI" in res.final_output
        assert "Showing verified reference content" in res.final_output
