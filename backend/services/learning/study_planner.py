"""
Study Planner Agent Service (Feature 11 — Phase C)

Creates a personalized subset of tasks (daily, weekly) based on
enrolled courses and Phase B learning path data. Local logic only.
"""

from backend.models import Enrollment

def generate_study_plan(user_id: int) -> dict:
    """
    Generates a structured plan including daily tasks, weekly goals,
    and estimated hours.
    
    Returns:
        {
            "daily_tasks": ["..."],
            "weekly_goals": ["..."],
            "estimated_hours": int
        }
    """
    # 1. Fetch current enrollments
    enrollments = Enrollment.query.filter_by(user_id=user_id).all()
    in_progress_enrollments = [
        e for e in enrollments 
        if not e.completed and ((e.progress_percentage or e.progress or 0) < 100)
    ]
    
    daily_tasks = []
    weekly_goals = []
    estimated_hours = 0
    
    # 2. Build tasks based on current progress
    if in_progress_enrollments:
        # Pick the most active course or just the first incomplete one
        active_enrollment = in_progress_enrollments[0]
        course = active_enrollment.course
        
        if course:
            daily_tasks.append(f"Watch the next lesson in '{course.title}'.")
            daily_tasks.append("Review your flashcards / notes for 15 minutes.")
            
            # Simple heuristic for weekly goals
            progress_pct = active_enrollment.progress_percentage or active_enrollment.progress or 0
            if progress_pct < 20:
                weekly_goals.append(f"Reach 50% completion in '{course.title}'.")
            elif progress_pct < 80:
                weekly_goals.append(f"Finish '{course.title}' by this weekend.")
            else:
                weekly_goals.append(f"Complete the final assignment for '{course.title}'.")
                
            weekly_goals.append("Attempt at least 2 coding challenges.")
            estimated_hours = 5
    else:
        # They have no active courses, perhaps completed everything or just starting
        # Let's import Phase B's path generator dynamically
        try:
            from services.learning.path_generator import generate_learning_path
            path_data = generate_learning_path(user_id)
            next_courses = path_data.get('next_courses', [])
            
            if next_courses:
                daily_tasks.append(f"Enroll in your recommended course: '{next_courses[0]['title']}'.")
                weekly_goals.append(f"Complete the first module of '{next_courses[0]['title']}'.")
                estimated_hours = 3
            else:
                daily_tasks.append("Explore the dashboard to find a topic that interests you.")
                weekly_goals.append("Start a new course tailored to your resume skills.")
                estimated_hours = 1
        except Exception:
            daily_tasks.append("Explore the course catalog to start learning.")
            weekly_goals.append("Try completing an introductory course.")
            estimated_hours = 2

    # Provide fallback tasks if list is empty
    if not daily_tasks:
        daily_tasks.append("Work on a personal coding project.")
    if not weekly_goals:
        weekly_goals.append("Practice your problem solving skills.")
        
    return {
        "daily_tasks": daily_tasks,
        "weekly_goals": weekly_goals,
        "estimated_hours": estimated_hours
    }
