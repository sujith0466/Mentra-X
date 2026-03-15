from __future__ import annotations

import random
from typing import Dict, List, Optional


class AIMentorService:
    """Rule-based mentor service used by both chatbot endpoints."""

    knowledge_base: Dict[str, str] = {
        "courses": "Mentra courses are organized by domain, modules, lessons, quizzes, and assignments so you can learn in a structured way.",
        "certificates": "You can download a certificate after completing a course. Finish the lessons and reach full progress to unlock it.",
        "assignments": "Assignments help you apply what you learn. Submit text answers or files, then review feedback once grading is complete.",
        "quizzes": "Quizzes test your understanding with timed attempts, pass percentages, and result tracking inside each enrolled course.",
        "learning streak": "Your learning streak grows when you complete lessons, quizzes, or assignments on consecutive days.",
        "referral": "Each student gets a referral code. When someone registers using it, both users can receive wallet rewards.",
        "career": "Mentra can guide you from beginner learning to role-based growth with courses, projects, roadmaps, resume analysis, and portfolio support.",
        "project ideas": "Project ideas work best when they match your domain and current level. Start with one focused build, then add advanced features.",
        "study tips": "Study in short focused sessions, complete lessons in sequence, review notes, and practice with quizzes or assignments.",
        "course recommendation": "Course recommendations should follow your enrolled domains, completion history, and progress gaps so your next step feels natural.",
        "portfolio": "A strong portfolio should show 2-4 real projects, clear problem statements, your role, and the technologies you used. You can use the Portfolio Builder from the AI Career Tools section.",
        "resume": "A good tech resume should highlight skills, projects, impact, and the technologies you used instead of listing only theory. Use the Resume Analyzer in AI Career Tools to review it.",
        "roadmap": "A career roadmap should combine foundational skills, guided courses, milestone projects, and consistent practice over time.",
        "skill gap": "A skill gap report compares your current completed learning with a target role and shows what skills, courses, and projects you should focus on next.",
        "coding practice": "Coding practice is strongest when you solve small problems consistently, compare your answer with a reference approach, and then refine your own solution.",
        "debugging": "Debugging gets easier when you identify the exact exception, read the traceback carefully, and isolate the variable or line causing the failure.",
        "codebase explainer": "A codebase explainer can summarize architecture, point out important files, and suggest how the project is organized.",
    }

    homepage_responses: Dict[str, str] = {
        "courses": "You can browse published courses from the catalog, explore domains, and view details before enrolling.",
        "certificates": "Mentra offers course certificates for students who complete their learning path.",
        "career": "Mentra supports career growth through learning paths, project ideas, roadmaps, resume analysis, and portfolio guidance.",
        "project ideas": "I can suggest project ideas based on domains like AI, Web Development, Python, Data Science, Machine Learning, and Cybersecurity.",
        "course recommendation": "Once you start learning, I can suggest the next best courses based on your enrollments and completed work.",
        "coding practice": "The Developer Tools section gives you topic-based coding problems so you can practice Python, Flask, SQL, algorithms, and data structures.",
    }

    dashboard_responses: Dict[str, str] = {
        "learning streak": "Your dashboard streak is driven by consistent activity. Complete one lesson or assessment daily to keep momentum going.",
        "study tips": "Use your dashboard to continue the next lesson, finish one active course before starting too many new ones, and review weak areas with quizzes.",
        "course recommendation": "Dashboard recommendations work best when they extend your current domain or fill a visible skill gap in your progress.",
        "career": "Use your completed courses, quiz outcomes, and projects together. Employers care more about applied proof than raw course count.",
        "portfolio": "Your dashboard now links directly to the Portfolio Builder so you can turn Mentra progress into a shareable profile draft.",
        "resume": "The Resume Analyzer can help you spot missing skills and strengthen how you describe your projects.",
        "skill gap": "Use the Skill Gap Detector to compare your current learning evidence with a target role like AI Engineer or Full Stack Developer.",
        "coding practice": "Use Coding Practice from Developer Tools to stay sharp between lessons and turn theory into actual problem solving.",
        "debugging": "The Debugging Assistant can help you interpret Python errors and narrow down likely fixes before you get stuck.",
        "codebase explainer": "The Codebase Explainer is useful when you want to understand an uploaded project structure before editing it.",
    }

    context_options: Dict[str, List[str]] = {
        "homepage": [
            "Which course should I start with?",
            "What project ideas can I build?",
            "How do certificates work?",
        ],
        "course": [
            "What should I learn first in this course?",
            "How do quizzes and assignments help me?",
            "What project can I build after this course?",
        ],
        "dashboard": [
            "How can I improve my progress?",
            "Recommend my next course",
            "How do I build a portfolio?",
        ],
        "general": [
            "Give me study tips",
            "How do I practice coding?",
            "How do I improve my resume?",
        ],
    }

    domain_project_ideas: Dict[str, List[str]] = {
        "Web Development": [
            "Build a portfolio website with project filtering and contact forms.",
            "Create a course marketplace with enrollment and progress tracking.",
        ],
        "Artificial Intelligence": [
            "Create a rule-based AI mentor for students in one domain.",
            "Build a study planner that generates tasks based on weak areas.",
        ],
        "Data Science": [
            "Analyze student performance trends with dashboards and summaries.",
            "Build a recommendation engine for courses based on learning history.",
        ],
        "Cyber Security": [
            "Create a security awareness tracker with quizzes and scorecards.",
            "Build a password audit training dashboard with risk categories.",
        ],
        "Cloud Computing": [
            "Design a deployment checklist system for web projects.",
            "Build an infrastructure learning tracker with roadmap milestones.",
        ],
        "Mobile App Development": [
            "Create a habit tracker app with streaks and push-style reminders.",
            "Build a student micro-learning app with lesson cards and quizzes.",
        ],
        "Python": [
            "Build a CLI learning tracker that records lessons and quiz scores.",
            "Create an automation script that summarizes study schedules.",
        ],
        "Machine Learning": [
            "Build a model comparison dashboard for simple classification tasks.",
            "Create a dataset explorer with preprocessing suggestions.",
        ],
    }

    role_roadmaps: Dict[str, List[str]] = {
        "full stack developer": ["HTML/CSS", "JavaScript", "Flask or Node", "Databases", "APIs", "Deployment"],
        "data scientist": ["Python", "Statistics", "Pandas", "Visualization", "Machine Learning", "Model storytelling"],
        "ai engineer": ["Python", "Math foundations", "Machine Learning", "Deep Learning", "Model evaluation", "Deployment basics"],
        "backend developer": ["Python", "Flask", "REST APIs", "SQL", "Authentication", "System design basics"],
        "frontend developer": ["HTML", "CSS", "JavaScript", "React", "Accessibility", "Performance"],
    }

    def _normalize_context(self, current_page: Optional[str]) -> str:
        page = (current_page or "").lower()
        if "home" in page:
            return "homepage"
        if "course" in page:
            return "course"
        if "dashboard" in page:
            return "dashboard"
        return "general"

    def _detect_domain(self, domain: Optional[str], course_name: Optional[str], message: str) -> Optional[str]:
        candidates = [domain or "", course_name or "", message]
        lowered = " ".join(candidates).lower()
        mapping = {
            "Web Development": ["web", "frontend", "backend", "flask", "javascript", "react"],
            "Data Science": ["data science", "analytics", "pandas", "numpy", "power bi"],
            "Artificial Intelligence": ["ai", "artificial intelligence", "deep learning", "nlp"],
            "Cyber Security": ["cyber", "security", "hacking", "network security"],
            "Cloud Computing": ["cloud", "aws", "docker", "kubernetes"],
            "Mobile App Development": ["mobile", "flutter", "react native", "android", "ios"],
            "Python": ["python"],
            "Machine Learning": ["machine learning", "ml"],
        }
        for label, keywords in mapping.items():
            if any(keyword in lowered for keyword in keywords):
                return label
        return domain

    def _match_topics(self, message: str) -> List[str]:
        matched = []
        synonyms = {
            "courses": ["course", "courses", "module", "lesson", "video", "syllabus"],
            "certificates": ["certificate", "certificates", "completion"],
            "assignments": ["assignment", "assignments", "submit", "submission", "feedback"],
            "quizzes": ["quiz", "quizzes", "attempt", "score", "passing"],
            "learning streak": ["streak", "consistency", "daily learning"],
            "referral": ["referral", "wallet", "reward", "bonus", "invite"],
            "career": ["career", "job", "role", "future", "path"],
            "project ideas": ["project", "project idea", "build"],
            "study tips": ["study", "study tips", "learn better", "improve", "focus"],
            "course recommendation": ["recommend", "recommendation", "next course", "what should i learn next"],
            "portfolio": ["portfolio", "showcase"],
            "resume": ["resume", "cv"],
            "roadmap": ["roadmap", "plan", "timeline"],
            "skill gap": ["skill gap", "skills do i need", "missing skills", "what skills do i need"],
            "coding practice": ["practice coding", "coding practice", "practice problem", "algorithm question"],
            "debugging": ["debug", "error", "traceback", "fix this python error"],
            "codebase explainer": ["codebase", "project structure", "architecture", "explain project"],
        }
        for topic, words in synonyms.items():
            if any(word in message for word in words):
                matched.append(topic)
        return matched

    def get_structured_response(
        self,
        message: str,
        *,
        current_page: Optional[str] = None,
        course_name: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> Dict[str, object]:
        normalized_message = (message or "").strip().lower()
        context = self._normalize_context(current_page)
        detected_domain = self._detect_domain(domain, course_name, normalized_message)
        matched_topics = self._match_topics(normalized_message)

        if any(word in normalized_message for word in ["hello", "hi", "hey", "namaste"]):
            answer = self._build_greeting(context, detected_domain, course_name)
            return {"answer": answer, "options": self.context_options[context]}

        if any(word in normalized_message for word in ["thanks", "thank you", "appreciate"]):
            return {
                "answer": "You're welcome. Keep moving one lesson at a time and ask whenever you need guidance.",
                "options": self.context_options[context],
            }

        if matched_topics:
            topic = matched_topics[0]
            answer = self._build_topic_response(topic, context, detected_domain, course_name)
            options = self._options_for_topic(topic, context)
            return {"answer": answer, "options": options}

        answer = self._fallback_response(context, detected_domain, course_name)
        return {"answer": answer, "options": self.context_options[context]}

    def get_text_response(
        self,
        message: str,
        *,
        current_page: Optional[str] = None,
        course_name: Optional[str] = None,
        domain: Optional[str] = None,
    ) -> str:
        payload = self.get_structured_response(
            message,
            current_page=current_page,
            course_name=course_name,
            domain=domain,
        )
        answer = str(payload["answer"])
        options = payload.get("options") or []
        if options:
            answer += "\n\nSuggested next questions:\n" + "\n".join(f"- {item}" for item in options[:3])
        return answer

    def _build_greeting(self, context: str, domain: Optional[str], course_name: Optional[str]) -> str:
        if context == "homepage":
            return "Hello! I can help you explore courses, understand how Mentra works, suggest project ideas, guide your career direction, and point you to developer tools."
        if context == "course" and course_name:
            return f"You're viewing {course_name}. I can explain the learning flow, quiz and assignment value, and what you can build after this course."
        if context == "dashboard":
            return "Welcome back. I can help you improve progress, plan your next course, generate project ideas, map a career path, or open the right developer tool from your dashboard."
        if domain:
            return f"Hello! I can help you learn {domain}, choose projects, practice coding, and plan your next steps."
        return "Hello! I can help with courses, quizzes, assignments, career planning, coding practice, debugging, codebase analysis, resumes, and portfolios."

    def _build_topic_response(self, topic: str, context: str, domain: Optional[str], course_name: Optional[str]) -> str:
        base = self.knowledge_base.get(topic, "I can help you with that.")
        context_map = {
            "homepage": self.homepage_responses,
            "dashboard": self.dashboard_responses,
        }
        contextual = context_map.get(context, {}).get(topic)

        parts = [base]
        if contextual:
            parts.append(contextual)
        if context == "course" and course_name:
            parts.append(f"For {course_name}, focus on finishing lessons in order and using quizzes or assignments to validate understanding.")
        if topic == "project ideas" and domain:
            ideas = self.domain_project_ideas.get(domain, [])
            if ideas:
                parts.append("Good starting directions:")
                parts.extend(f"- {idea}" for idea in ideas[:2])
        if topic in {"career", "roadmap"} and domain:
            parts.append(f"If you're interested in {domain}, combine guided courses with at least two practical projects.")
        if topic == "portfolio":
            parts.append("Open the Portfolio Builder from AI Career Tools to turn your completed courses and project ideas into a draft showcase.")
        if topic == "resume":
            parts.append("Open the Resume Analyzer from AI Career Tools to review your resume text and spot missing skills.")
        if topic == "skill gap":
            parts.append("Open the Skill Gap Detector from AI Career Tools to compare your current progress with a target role.")
        if topic == "coding practice":
            parts.append("Open Coding Practice from Developer Tools to get a topic-based problem and write your own attempt.")
        if topic == "debugging":
            parts.append("Open the Debugging Assistant from Developer Tools and paste the error message or traceback for a rule-based explanation.")
        if topic == "codebase explainer":
            parts.append("Open the Codebase Explainer from Developer Tools and upload a ZIP or paste file names to get an architecture summary.")
        return "\n\n".join(parts)

    def _options_for_topic(self, topic: str, context: str) -> List[str]:
        topic_specific = {
            "courses": ["How do I choose the right course?", "Recommend my next course", "How do certificates work?"],
            "certificates": ["How do I complete a course faster?", "What counts toward progress?", "Recommend my next course"],
            "assignments": ["How should I prepare for assignments?", "How do quizzes help?", "Give me study tips"],
            "quizzes": ["How do I score better in quizzes?", "How should I revise lessons?", "Recommend a project idea"],
            "learning streak": ["How can I stay consistent?", "Give me study tips", "Create a career roadmap for me"],
            "referral": ["How do wallet rewards work?", "How do I share my referral link?", "What should I learn next?"],
            "career": ["Create a career roadmap for me", "How do I improve my resume?", "What courses should I take next?"],
            "project ideas": ["Give me web development project ideas", "Give me AI project ideas", "How do I build a portfolio?"],
            "study tips": ["How do I improve my progress?", "How should I revise for quizzes?", "Recommend my next course"],
            "course recommendation": ["Recommend my next course", "Create a career roadmap for me", "Give me project ideas for my domain"],
            "portfolio": ["What should I include in my portfolio?", "How do I improve my resume?", "Show my skill gaps"],
            "resume": ["What projects strengthen my resume?", "How do I build a portfolio?", "Show my skill gaps"],
            "roadmap": ["Create a roadmap for Full Stack Developer", "Create a roadmap for Data Scientist", "Recommend courses for my path"],
            "skill gap": ["What skills do I need for AI Engineer?", "Show my skill gaps", "How do I build a portfolio?"],
            "coding practice": ["Give me a Python coding problem", "How do I practice Flask?", "How do I fix this Python error?"],
            "debugging": ["How do I fix this Python error?", "How do I practice coding?", "How do I analyze a codebase?"],
            "codebase explainer": ["Explain my project structure", "How do I map my modules?", "How do I improve my resume?"],
        }
        return topic_specific.get(topic, self.context_options.get(context, self.context_options["general"]))

    def _fallback_response(self, context: str, domain: Optional[str], course_name: Optional[str]) -> str:
        fallbacks = [
            "I can help with course guidance, quizzes, assignments, certificates, referrals, project ideas, recommendations, resumes, skill gaps, coding practice, debugging, and codebase analysis.",
            "Try asking about study tips, your next course, a project idea, your resume, a portfolio, coding practice, debugging, or codebase analysis.",
            "Ask me something learning-focused, career-focused, or developer-focused, such as how to improve progress, what to build next, how to fix an error, or which projects your portfolio is missing.",
        ]
        response = random.choice(fallbacks)
        if context == "course" and course_name:
            response += f" Since you're on {course_name}, I can also explain what to do after finishing this course."
        if context == "dashboard":
            response += " On the dashboard, I can guide you using your learning progress context."
        if domain:
            response += f" I also detected interest in {domain}."
        return response


mentor_service = AIMentorService()

