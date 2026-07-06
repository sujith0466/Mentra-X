"""
Mentra X — Unit & Integration Tests for Milestone 6.1 (Adaptive Learning Intelligence Core)
Tests 5-level pedagogical escalation, style detection math, dynamic prompt generation,
and API route contracts.
"""

import pytest
import json
from backend.services.adaptive.dto import AvoidanceConstraintsDTO, TutorDecisionDTO, PersonalizationBundleDTO
from backend.services.adaptive.tutor_decision_engine import TutorDecisionEngine
from backend.services.adaptive.learning_style_detector import LearningStyleDetector
from backend.services.adaptive.dynamic_prompt_builder import DynamicPromptBuilder
from backend.services.adaptive.personalization_engine import PersonalizationEngine
from backend.services.orchestration.tools.registry import ToolRegistry
from backend.services.orchestration.tools.tutor_tools import register_tutor_tools


class TestAdaptiveCoreDTOs:
    def test_dto_serialization(self):
        constraints = AvoidanceConstraintsDTO(levels_to_avoid=[2], analogies_to_avoid=["nesting_dolls"], analogies_that_worked=["trees"])
        decision = TutorDecisionDTO(
            level=4,
            level_name="Visual Analogy",
            strategy="Concrete, tangible",
            rationale="Escalated due to prior failure",
            constraints=constraints,
            adjusted_mastery=0.42
        )
        data = decision.to_dict()
        assert data["level"] == 4
        assert data["constraints"]["levels_to_avoid"] == [2]

        restored = TutorDecisionDTO.from_dict(data)
        assert restored.level == 4
        assert restored.constraints.analogies_to_avoid == ["nesting_dolls"]


class TestTutorDecisionEngine:
    def setup_method(self):
        self.engine = TutorDecisionEngine()

    def test_level_1_high_mastery(self):
        dna = {"mastery_per_concept": {"recursion": 0.85}}
        decision = self.engine.select_level("recursion", dna)
        assert decision.level == 1
        assert decision.level_name == "Direct"

    def test_level_2_moderate_mastery(self):
        dna = {"mastery_per_concept": {"recursion": 0.55}}
        decision = self.engine.select_level("recursion", dna)
        assert decision.level == 2
        assert decision.level_name == "Worked Example"

    def test_level_3_low_mastery(self):
        dna = {"mastery_per_concept": {"recursion": 0.30}}
        decision = self.engine.select_level("recursion", dna)
        assert decision.level == 3
        assert decision.level_name == "Mistake Analysis"

    def test_critical_weakness_jump_to_level_4(self):
        dna = {"mastery_per_concept": {"recursion": 0.60}}
        weak = [{"concept": "recursion", "severity": "CRITICAL"}]
        decision = self.engine.select_level("recursion", dna, weak_concepts=weak)
        assert decision.level == 4
        assert "CRITICAL" in decision.rationale

    def test_consecutive_failures_escalation(self):
        dna = {"mastery_per_concept": {"recursion": 0.50}}
        history = [
            {"concept": "recursion", "selected_level": 2, "outcome_success": False},
            {"concept": "recursion", "selected_level": 2, "outcome_success": False}
        ]
        decision = self.engine.select_level("recursion", dna, explanation_history=history)
        assert decision.level == 4  # Escalated by 2 from Level 2

    def test_avoidance_constraints_skipping(self):
        dna = {"mastery_per_concept": {"recursion": 0.55}} # normally Level 2
        history = [
            {"concept": "recursion", "selected_level": 2, "outcome_success": False, "analogy_used": "boxes"}
        ]
        decision = self.engine.select_level("recursion", dna, explanation_history=history)
        assert decision.level == 3  # Shifted from 2 to 3 to avoid failed level
        assert 2 in decision.constraints.levels_to_avoid
        assert "boxes" in decision.constraints.analogies_to_avoid


class TestLearningStyleDetector:
    def setup_method(self):
        self.detector = LearningStyleDetector()

    def test_visual_style_detection(self):
        style, conf = self.detector.detect_style(
            session_response_times=[30.0, 35.0],
            answer_patterns=["I need a diagram or picture to imagine the shape"],
            quiz_errors=[]
        )
        assert style == "Visual"
        assert conf > 0.5

    def test_math_style_detection(self):
        style, conf = self.detector.detect_style(
            session_response_times=[8.0, 10.0],
            answer_patterns=["What is the formula and step calculation?"],
            quiz_errors=[]
        )
        assert style == "Mathematical"
        assert conf > 0.5


class TestDynamicPromptBuilder:
    def setup_method(self):
        self.builder = DynamicPromptBuilder()

    def test_prompt_templating(self):
        dna = {"mastery_per_concept": {"recursion": 0.40}}
        constraints = AvoidanceConstraintsDTO(analogies_to_avoid=["dolls"], analogies_that_worked=["trees"])
        prompt = self.builder.build("recursion", level=4, dna=dna, constraints=constraints, style="Visual")
        assert "[SYSTEM PEDAGOGICAL INSTRUCTION — LEVEL 4]" in prompt
        assert "real-world visual analogy" in prompt
        assert "trees" in prompt
        assert "dolls" in prompt
        assert "Emphasize visual metaphors" in prompt


class TestPersonalizationEngineAndTools:
    def setup_method(self):
        self.engine = PersonalizationEngine()

    def test_assemble_bundle(self):
        bundle = self.engine.assemble_personalization_bundle(
            user_id="test_usr",
            concept="recursion",
            dna={"mastery_per_concept": {"recursion": 0.20}, "preferred_style": "Visual"},
            explanation_history=[]
        )
        assert isinstance(bundle, PersonalizationBundleDTO)
        assert bundle.selected_level == 4  # Low mastery (Level 3) + Visual preference -> Level 4
        assert bundle.selected_style == "Visual"
        assert "recursion" in bundle.system_prompt

    def test_mastra_tutor_tool_registration_and_execution(self):
        registry = ToolRegistry()
        registry.clear()
        register_tutor_tools(registry)
        
        tools = registry.get_all_tools()
        assert "selectExplanationLevel" in tools
        
        res = registry.execute_tool(
            "selectExplanationLevel", 
            kwargs={"user_id": "usr_10", "concept": "recursion", "dna": {"mastery_per_concept": {"recursion": 0.80}}}
        )
        assert res["selected_level"] == 1
        assert "Direct" in res["level_name"]


class TestAdaptiveRoutes:
    @pytest.fixture
    def client(self):
        from backend.app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_evaluate_endpoint(self, client):
        payload = {
            "user_id": "usr_api",
            "concept": "recursion",
            "dna": {"mastery_per_concept": {"recursion": 0.50}},
            "session_response_times": [10.0, 9.0],
            "answer_patterns": ["show me the formula"]
        }
        resp = client.post('/api/v1/adaptive/evaluate', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["bundle"]["selected_style"] == "Mathematical"
        assert data["bundle"]["selected_level"] == 2

    def test_get_session_decision_endpoint(self, client):
        resp = client.get('/api/v1/adaptive/decision/sess_998877?concept=recursion')
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["session_id"] == "sess_998877"
        assert "selected_level" in data["decision"]
