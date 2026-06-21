from __future__ import annotations

from typing import Optional

from backend.models import Enrollment
from backend.services.ai.agents.base_agent import BaseAgent
from backend.services.ai.learning.study_planner_service import (
    generate_adaptive_learning_path,
    generate_adaptive_study_plan,
)
from backend.services.ai.ml.learning_difficulty_model import detect_learning_difficulty
from backend.services.ai.ml.recommendation_model import recommend_courses_ml
from backend.services.ai.ml.skill_prediction_model import predict_next_skills
from backend.services.ai.skills.skill_graph_service import get_skill_progress_snapshot


class LearningAgent(BaseAgent):
    agent_name = "learning"

    @staticmethod
    def _active_course_id(user_id: Optional[int]) -> Optional[int]:
        if not user_id:
            return None
        enrollments = Enrollment.query.filter_by(user_id=user_id).all()
        for enrollment in enrollments:
            progress = enrollment.progress_percentage or enrollment.progress or 0
            if enrollment.course_id and progress < 100:
                return enrollment.course_id
        return enrollments[0].course_id if enrollments else None

    def handle(self, user_id: Optional[int], message: str, **kwargs):
        intent = kwargs.get("intent", "study_help")

        if user_id and intent == "study_help":
            course_id = self._active_course_id(user_id)
            difficulty = detect_learning_difficulty(user_id) or {}
            if course_id:
                plan = generate_adaptive_study_plan(user_id, course_id)
                first_days = [
                    f"Day {item['day']}: {', '.join(item['lessons'])}"
                    for item in plan.get("days", [])[:2]
                ]
                answer = "Adaptive study plan ready. "
                if first_days:
                    answer += "Next steps: " + " | ".join(first_days)
                else:
                    answer += "You are close to completion, so focus on revision and one light study block per day."
                if difficulty.get("weak_topics"):
                    answer += " Weak topics: " + ", ".join(difficulty["weak_topics"][:3]) + "."
                return self.build_response(
                    answer,
                    suggestions=["Show my weak topics", "Recommend revision steps", "What should I learn next?"],
                    data=plan,
                    intent=intent,
                )

        if user_id and intent == "learning_path":
            path = generate_adaptive_learning_path(user_id)
            answer = "Adaptive learning path: "
            if path.get("recommended_lessons"):
                answer += "Lessons to focus on: " + ", ".join(path["recommended_lessons"][:3]) + ". "
            if path.get("recommended_quizzes"):
                answer += "Practice quizzes: " + ", ".join(path["recommended_quizzes"][:2]) + ". "
            if path.get("revision_topics"):
                answer += "Revision topics: " + ", ".join(path["revision_topics"][:2]) + "."
            return self.build_response(
                answer.strip(),
                suggestions=["Show my weak topics", "Show my learning progress", "Recommend my next course"],
                data=path,
                intent=intent,
            )

        if user_id and intent == "skill_progress":
            skills = get_skill_progress_snapshot(user_id)
            top_skills = skills[:4]
            answer = "Your current skill progress: "
            if top_skills:
                answer += "; ".join(
                    f"{item['skill_name']} {int(item['progress_percentage'])}%"
                    for item in top_skills
                ) + "."
            else:
                answer += "Your skill graph will grow as you complete lessons, quizzes, coding, and interviews."
            return self.build_response(
                answer.strip(),
                suggestions=["What skills should I learn next?", "Show my learning path", "Recommend my next course"],
                data={"skills": skills},
                intent=intent,
            )

        if user_id and intent == "course_recommendation":
            recommendations = recommend_courses_ml(user_id)
            top_courses = recommendations.get("recommended_courses", [])[:3]
            if top_courses:
                answer = "Recommended next courses: " + ", ".join(item["title"] for item in top_courses) + "."
            else:
                answer = "I could not find a strong personalized course match yet, so start with your current domain's next published course."
            return self.build_response(
                answer,
                suggestions=["Why these courses?", "Show my skill gaps", "Give me project ideas"],
                data=recommendations,
                intent=intent,
            )

        if user_id:
            difficulty = detect_learning_difficulty(user_id) or {}
            skill_prediction = predict_next_skills(user_id) or {}
            answer = "Learning support is ready."
            if difficulty.get("weak_topics"):
                answer += " Review " + ", ".join(difficulty["weak_topics"][:2]) + "."
            if skill_prediction.get("skills_to_learn_next"):
                answer += " Next skills: " + ", ".join(skill_prediction["skills_to_learn_next"][:3]) + "."
            return self.build_response(
                answer,
                suggestions=["Build a study plan", "Show my learning progress", "Recommend my next course"],
                data={"difficulty": difficulty, "skill_prediction": skill_prediction},
                intent=intent,
            )

        return self.build_response(
            "Sign in as a student to unlock your adaptive study plan, skill graph progress, and course recommendations.",
            suggestions=["Browse courses", "Show study planner", "Open skill graph"],
            intent=intent,
        )
