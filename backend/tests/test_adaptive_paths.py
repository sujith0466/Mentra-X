"""
Mentra X — Unit & Integration Tests for Milestone 6.2 (Personalized Learning Paths)
Tests dynamic syllabus re-ordering, prerequisite priority promotion, and study
velocity goal calculations.
"""

import pytest
from backend.services.adaptive.path_optimizer import DynamicRoadmapGenerator, LessonProjectionDTO
from backend.services.adaptive.goal_planner import GoalPlanner
from backend.services.orchestration.tools.registry import ToolRegistry
from backend.services.orchestration.tools.path_tools import register_path_tools


class TestDynamicRoadmapGenerator:
    def setup_method(self):
        self.generator = DynamicRoadmapGenerator()
        self.sample_lessons = [
            {"id": 101, "title": "Intro to Python", "concept": "python_syntax", "order": 1},
            {"id": 102, "title": "Loops and Iteration", "concept": "loops", "order": 2},
            {"id": 103, "title": "Recursion Depth", "concept": "recursion", "order": 3},
            {"id": 104, "title": "Dynamic Programming", "concept": "dp", "order": 4}
        ]

    def test_prerequisite_reordering(self):
        # Suppose student has low mastery in recursion (0.35) and high mastery in python_syntax (0.90)
        dna = {
            "mastery_per_concept": {
                "python_syntax": 0.90,
                "loops": 0.70,
                "recursion": 0.35,
                "dp": 0.65
            }
        }
        projections = self.generator.generate_roadmap(
            course_id=1,
            lessons=self.sample_lessons,
            dna=dna,
            completed_lesson_ids=[101] # Intro completed
        )
        
        assert len(projections) == 4
        # Recursion should move to the top of incomplete lessons ("URGENT_PREREQ")
        assert projections[0].lesson_id == 103
        assert projections[0].status == "URGENT_PREREQ"
        assert projections[0].recommended_order == 1
        
        # Completed lesson 101 should be at the very bottom
        assert projections[-1].lesson_id == 101
        assert projections[-1].status == "COMPLETED"


class TestGoalPlanner:
    def setup_method(self):
        self.planner = GoalPlanner()

    def test_velocity_achievable(self):
        res = self.planner.calculate_study_velocity(remaining_lessons=10, target_deadline_iso="2026-12-31T00:00:00Z")
        assert res["status"] == "ACTIVE"
        assert res["feasibility"] in ("ACHIEVABLE", "CHALLENGING")
        assert res["required_lessons_per_week"] > 0

    def test_velocity_completed(self):
        res = self.planner.calculate_study_velocity(remaining_lessons=0, target_deadline_iso="2026-12-31T00:00:00Z")
        assert res["status"] == "COMPLETED"
        assert res["required_hours_per_week"] == 0.0


class TestPathToolsAndRoutes:
    def test_mastra_path_tools(self):
        registry = ToolRegistry()
        registry.clear()
        register_path_tools(registry)
        
        tools = registry.get_all_tools()
        assert "getPersonalizedRoadmap" in tools
        assert "calculateStudyVelocity" in tools
        
        roadmap = registry.execute_tool(
            "getPersonalizedRoadmap",
            kwargs={
                "course_id": 1,
                "lessons": [{"id": 1, "title": "Test Lesson", "concept": "test", "order": 1}],
                "dna": {"mastery_per_concept": {"test": 0.20}}
            }
        )
        assert len(roadmap) == 1
        assert roadmap[0]["status"] == "URGENT_PREREQ"

    @pytest.fixture
    def client(self):
        from backend.app import app
        app.config['TESTING'] = True
        with app.test_client() as client:
            yield client

    def test_path_route(self, client):
        payload = {
            "lessons": [{"id": 10, "title": "Loops", "concept": "loops", "order": 1}],
            "dna": {"mastery_per_concept": {"loops": 0.40}}
        }
        resp = client.post('/api/v1/adaptive/paths/5', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert data["roadmap"][0]["status"] == "URGENT_PREREQ"

    def test_velocity_route(self, client):
        payload = {"remaining_lessons": 12, "target_deadline_iso": "2026-10-01T00:00:00Z"}
        resp = client.post('/api/v1/adaptive/velocity', json=payload)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "success"
        assert "required_lessons_per_week" in data["velocity"]
