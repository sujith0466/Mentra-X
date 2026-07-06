"""
Mentra X — Adaptive Learning Intelligence API Routes (Phase 6)
URL Prefix: /api/v1/adaptive

Exposes enterprise endpoints for pedagogical level evaluation, style detection,
dynamic study roadmaps, progressive coding hints, pace/fatigue status, and
unified recommendations.
"""

from flask import Blueprint, request, jsonify, session
from backend.services.adaptive.personalization_engine import PersonalizationEngine
from backend.services.adaptive.tutor_decision_engine import TutorDecisionEngine
from backend.services.adaptive.learning_style_detector import LearningStyleDetector
from backend.services.adaptive.path_optimizer import DynamicRoadmapGenerator
from backend.services.adaptive.goal_planner import GoalPlanner
from backend.services.adaptive.content_selector import ContentRankingEngine
from backend.services.adaptive.prerequisite_engine import PrerequisiteEngine
from backend.services.adaptive.feedback_engine import ProgressiveHintEngine, SocraticFeedbackEngine
from backend.services.adaptive.pacing_engine import FatigueDetector, SpacedRepetitionScheduler
from backend.services.adaptive.recommendation_engine import UnifiedRecommendationEngine
import logging

logger = logging.getLogger(__name__)

adaptive_bp = Blueprint('adaptive', __name__, url_prefix='/api/v1/adaptive')
personalization_engine = PersonalizationEngine()
style_detector = LearningStyleDetector()
roadmap_generator = DynamicRoadmapGenerator()
goal_planner = GoalPlanner()
ranking_engine = ContentRankingEngine()
prereq_engine = PrerequisiteEngine()
hint_engine = ProgressiveHintEngine()
socratic_engine = SocraticFeedbackEngine()
fatigue_detector = FatigueDetector()
scheduler = SpacedRepetitionScheduler()
recommendation_engine = UnifiedRecommendationEngine()


@adaptive_bp.route('/evaluate', methods=['POST'])
def evaluate_personalization():
    """
    Evaluates student cognitive state and returns a PersonalizationBundleDTO.
    Consumes JSON: { user_id, concept, dna, explanation_history, weak_concepts }
    """
    try:
        data = request.get_json() or {}
        user_id = str(data.get("user_id") or session.get("user_id") or "")
        concept = str(data.get("concept") or "")
        if not concept:
            return jsonify({"status": "error", "message": "concept is required"}), 400

        bundle = personalization_engine.assemble_personalization_bundle(
            user_id=user_id,
            concept=concept,
            dna=data.get("dna"),
            explanation_history=data.get("explanation_history", []),
            weak_concepts=data.get("weak_concepts", []),
            session_response_times=data.get("session_response_times", []),
            answer_patterns=data.get("answer_patterns", []),
            quiz_errors=data.get("quiz_errors", [])
        )
        return jsonify({"status": "success", "bundle": bundle.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error in evaluate_personalization: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/decision/<session_id>', methods=['GET'])
def get_session_decision(session_id):
    """
    Inspects pedagogical rationale and decision state for a given tutoring session.
    """
    try:
        # In enterprise runtime, query MongoDB ai_sessions collection if available
        try:
            from backend.app import app
            if hasattr(app, "mongo_db") and app.mongo_db is not None:
                doc = app.mongo_db.ai_sessions.find_one({"session_id": session_id})
                if doc:
                    doc["_id"] = str(doc["_id"])
                    return jsonify({"status": "success", "decision": doc}), 200
        except Exception:
            pass

        # Fallback response for active sessions or unit tests
        concept = request.args.get("concept", "general")
        user_id = str(session.get("user_id") or request.args.get("user_id") or "")
        bundle = personalization_engine.assemble_personalization_bundle(
            user_id=user_id,
            concept=concept
        )
        return jsonify({
            "status": "success",
            "session_id": session_id,
            "decision": {
                "selected_level": bundle.selected_level,
                "level_name": bundle.level_name,
                "detected_style": bundle.selected_style,
                "teaching_rationale": bundle.teaching_rationale,
                "avoidance_constraints": bundle.avoidance_constraints
            }
        }), 200
    except Exception as e:
        logger.error(f"Error in get_session_decision: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/paths/<int:course_id>', methods=['GET', 'POST'])
def get_personalized_roadmap(course_id):
    """
    Returns re-ordered lesson sequence DTO for a course based on student mastery.
    """
    try:
        data = request.get_json(silent=True) or {}
        lessons = data.get("lessons", [])
        dna = data.get("dna", {})
        completed = data.get("completed_lesson_ids", [])

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
        return jsonify({"status": "success", "course_id": course_id, "roadmap": [p.to_dict() for p in projections]}), 200
    except Exception as e:
        logger.error(f"Error in get_personalized_roadmap: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/velocity', methods=['POST'])
def calculate_velocity():
    """
    Computes required study velocity given target deadline and remaining lessons.
    """
    try:
        data = request.get_json() or {}
        rem = int(data.get("remaining_lessons", 0))
        deadline = str(data.get("target_deadline_iso", ""))
        res = goal_planner.calculate_study_velocity(rem, deadline)
        return jsonify({"status": "success", "velocity": res}), 200
    except Exception as e:
        logger.error(f"Error in calculate_velocity: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/content/rank', methods=['POST'])
def rank_content():
    """
    Ranks learning resources by student fit.
    """
    try:
        data = request.get_json() or {}
        resources = data.get("resources", [])
        dna = data.get("dna", {})
        concept = str(data.get("concept", ""))
        failed = data.get("failed_resource_ids", [])
        dtos = ranking_engine.rank_resources(resources, dna, concept, failed)
        return jsonify({"status": "success", "ranked_resources": [d.to_dict() for d in dtos]}), 200
    except Exception as e:
        logger.error(f"Error in rank_content: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/prerequisites/check', methods=['POST'])
def check_prerequisites():
    """
    Checks if prerequisites are met for a target concept.
    """
    try:
        data = request.get_json() or {}
        concept = str(data.get("target_concept", ""))
        if not concept:
            return jsonify({"status": "error", "message": "target_concept is required"}), 400
        dna = data.get("dna", {})
        thresh = float(data.get("mastery_threshold", 0.60))
        res = prereq_engine.check_prerequisites(concept, dna, mastery_threshold=thresh)
        return jsonify({"status": "success", "prerequisite_check": res}), 200
    except Exception as e:
        logger.error(f"Error in check_prerequisites: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/hint', methods=['POST'])
def generate_hint():
    """
    Generates progressive hint for a student problem.
    """
    try:
        data = request.get_json() or {}
        concept = str(data.get("concept", ""))
        idx = int(data.get("current_hint_index", 0))
        ctx = data.get("problem_context")
        custom = data.get("custom_hints")
        dto = hint_engine.get_hint(concept, idx, ctx, custom)
        return jsonify({"status": "success", "hint": dto.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error in generate_hint: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/socratic', methods=['POST'])
def generate_socratic():
    """
    Formulates a guiding Socratic question.
    """
    try:
        data = request.get_json() or {}
        concept = str(data.get("concept", ""))
        ans = data.get("student_answer", "")
        rule = str(data.get("expected_concept_rule", ""))
        is_corr = bool(data.get("is_correct", False))
        dto = socratic_engine.generate_socratic_feedback(concept, ans, rule, is_corr)
        return jsonify({"status": "success", "socratic_feedback": dto.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error in generate_socratic: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/pace/fatigue', methods=['POST'])
def check_fatigue():
    """
    Monitors cognitive fatigue and burnout indicators.
    """
    try:
        data = request.get_json() or {}
        dur = float(data.get("session_duration_mins", 0))
        errs = int(data.get("recent_errors", 0))
        deg = float(data.get("response_time_degradation_pct", 0))
        dto = fatigue_detector.evaluate_fatigue(dur, errs, deg)
        return jsonify({"status": "success", "fatigue": dto.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error in check_fatigue: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/pace/schedule', methods=['POST'])
def schedule_review():
    """
    Calculates Ebbinghaus spaced repetition review schedule.
    """
    try:
        data = request.get_json() or {}
        concept = str(data.get("concept", ""))
        hours = float(data.get("hours_since_last_review", 0))
        mast = float(data.get("initial_mastery", 0.80))
        dto = scheduler.calculate_review_schedule(concept, hours, mast)
        return jsonify({"status": "success", "review_schedule": dto.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error in schedule_review: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500


@adaptive_bp.route('/recommendations', methods=['POST'])
def get_recommendations():
    """
    Returns unified, prioritized recommendation feed across all adaptive services.
    """
    try:
        data = request.get_json() or {}
        uid = str(data.get("user_id") or session.get("user_id") or "")
        concept = str(data.get("concept", "general"))
        dna = data.get("dna")
        dur = float(data.get("session_duration_mins", 0))
        errs = int(data.get("recent_errors", 0))
        lessons = data.get("lessons")
        res = data.get("resources")
        rev = data.get("review_concepts")
        dto = recommendation_engine.generate_feed(uid, concept, dna, dur, errs, 0.0, 1, lessons, res, rev)
        return jsonify({"status": "success", "recommendation_feed": dto.to_dict()}), 200
    except Exception as e:
        logger.error(f"Error in get_recommendations: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500





