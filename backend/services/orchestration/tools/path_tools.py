from backend.services.orchestration.tools.registry import ToolRegistry, ToolDefinition
from backend.services.adaptive.path_optimizer import DynamicRoadmapGenerator
from backend.services.adaptive.goal_planner import GoalPlanner
import logging

logger = logging.getLogger(__name__)

def register_path_tools(registry: ToolRegistry):
    roadmap_generator = DynamicRoadmapGenerator()
    goal_planner = GoalPlanner()

    get_roadmap_def = ToolDefinition(
        name="getPersonalizedRoadmap",
        description="Re-order course lessons based on student concept mastery without modifying database enrollments.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="course:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=["learning.roadmap_generated"],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "course_id": {"type": "integer"},
                "lessons": {"type": "array"},
                "dna": {"type": "object"},
                "completed_lesson_ids": {"type": "array"}
            },
            "required": ["course_id"]
        },
        output_schema={"type": "array"},
        timeout_ms=1500,
        retry_count=1
    )

    def get_roadmap_impl(kwargs: dict):
        course_id = int(kwargs.get("course_id", 1))
        lessons = kwargs.get("lessons", [])
        dna = kwargs.get("dna", {})
        completed = kwargs.get("completed_lesson_ids", [])

        # If lessons not passed directly, attempt to load from database
        if not lessons:
            try:
                from backend.models import Lesson
                db_lessons = Lesson.query.filter_by(course_id=course_id).order_by(Lesson.order).all()
                lessons = [{"id": l.id, "title": l.title, "concept": getattr(l, "concept", "") or l.title.lower().replace(" ", "_"), "order": l.order} for l in db_lessons]
            except Exception:
                lessons = []

        projections = roadmap_generator.generate_roadmap(
            course_id=course_id,
            lessons=lessons,
            dna=dna,
            completed_lesson_ids=completed
        )
        return [p.to_dict() for p in projections]

    calculate_velocity_def = ToolDefinition(
        name="calculateStudyVelocity",
        description="Calculate required study velocity (lessons/week) given a target completion deadline.",
        version="1.0.0",
        owner="AdaptiveLearningTeam",
        permissions="course:read",
        is_mutable=False,
        supports_streaming=False,
        supports_parallel=True,
        deterministic=True,
        needs_verification=False,
        produces_events=[],
        consumes_events=[],
        input_schema={
            "type": "object",
            "properties": {
                "remaining_lessons": {"type": "integer"},
                "target_deadline_iso": {"type": "string"}
            },
            "required": ["remaining_lessons", "target_deadline_iso"]
        },
        output_schema={"type": "object"},
        timeout_ms=1000,
        retry_count=1
    )

    def calculate_velocity_impl(kwargs: dict):
        rem = int(kwargs.get("remaining_lessons", 0))
        deadline = str(kwargs.get("target_deadline_iso", ""))
        return goal_planner.calculate_study_velocity(rem, deadline)

    registry.register_tool(get_roadmap_def, get_roadmap_impl)
    registry.register_tool(calculate_velocity_def, calculate_velocity_impl)
    logger.info("Registered path optimization tools.")
