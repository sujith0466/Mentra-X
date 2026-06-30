import json
from backend.models import (
    db, User, StudentTwinRecord, TwinKnowledgeStateRecord, UserXP, 
    Enrollment, QuizAttempt, SkillProgress, UserResume, InterviewSession, StudentProject,
    utcnow
)
from backend.services.twin.concept_resolver import ConceptResolver
from backend.services.twin.twin_model import (
    AcademicState, SkillState, LearningDNA, CareerState, ProjectState, OpportunityState
)

def build_initial_twin(user_id: int, exam_track: str = "JEE") -> StudentTwinRecord:
    """
    Initializes a new Digital Twin by performing a massive cross-table query
    of the student's historical LMS data to build the starting 7-state representation.
    """
    user = User.query.get(user_id)
    if not user:
        raise ValueError("User not found")
    
    existing_twin = db.session.query(StudentTwinRecord).filter_by(user_id=user_id).first()
    if existing_twin:
        return existing_twin
        
    twin = StudentTwinRecord(
        user_id=user_id,
        twin_version=1,
        twin_status='INITIALIZING',
        twin_health=0.0,
        exam_track=exam_track
    )
    db.session.add(twin)
    db.session.flush() # get ID
    
    # Academic State
    xp = UserXP.query.get(user_id)
    xp_total = xp.xp_points if xp else 0
    enrollments = db.session.query(Enrollment).filter_by(user_id=user_id).all()
    enrolled_courses = [e.course_id for e in enrollments]
    completion_rate = sum([e.progress for e in enrollments]) / len(enrollments) if enrollments else 0.0
    
    from backend.models import LearningStreak
    streak = db.session.query(LearningStreak).filter_by(user_id=user_id).first()
    streak_days = streak.current_streak if streak else 0
    
    academic_state = AcademicState(
        enrolled_courses=enrolled_courses,
        xp_total=xp_total,
        completion_rate=completion_rate,
        streak_days=streak_days
    )
    twin.academic_state = json.dumps(academic_state.__dict__)
    
    # Knowledge State -> populated in TwinKnowledgeStateRecord
    quiz_attempts = db.session.query(QuizAttempt).filter_by(user_id=user_id, passed=True).all()
    concept_map = {}
    for qa in quiz_attempts:
        concept = ConceptResolver.resolve_from_quiz(qa.quiz.title)
        # simplistic merge
        concept_map[concept] = max(concept_map.get(concept, 0.0), qa.score_percentage / 100.0)
    
    for concept, mastery in concept_map.items():
        ks = TwinKnowledgeStateRecord(
            twin_id=twin.id,
            concept_id=concept,
            mastery_score=mastery,
            last_reviewed=utcnow()
        )
        db.session.add(ks)
        
    # Skill State
    skills = db.session.query(SkillProgress).filter_by(user_id=user_id).all()
    skill_dict = {s.skill_name: s.progress_percentage for s in skills}
    twin.skill_state = json.dumps(SkillState(skills=skill_dict).__dict__)
    
    # Learning DNA
    twin.learning_dna = json.dumps(LearningDNA().__dict__)
    
    # Career State
    resume = db.session.query(UserResume).filter_by(user_id=user_id).first()
    extracted_skills = []
    if resume and resume.skills_json:
        try:
            extracted_skills = json.loads(resume.skills_json)
        except Exception:
            pass
            
    interviews = db.session.query(InterviewSession).filter_by(user_id=user_id).all()
    avg_score = sum([i.score for i in interviews]) / len(interviews) if interviews else 0.0
    twin.career_state = json.dumps(CareerState(skills_extracted=extracted_skills, interview_score_avg=avg_score).__dict__)
    
    # Project State
    projects = db.session.query(StudentProject).filter_by(user_id=user_id).all()
    project_dict = {p.project_id: p.progress_percentage for p in projects}
    twin.project_state = json.dumps(ProjectState(active_projects=project_dict).__dict__)
    
    # Opportunity State
    twin.opportunity_state = json.dumps(OpportunityState().__dict__)
    
    twin.twin_status = 'ACTIVE'
    
    # We must commit before health calculation so that the db sessions are fresh
    db.session.commit()
    
    from backend.services.twin.twin_health import compute_and_store_health
    compute_and_store_health(twin.id)
    
    return StudentTwinRecord.query.get(twin.id)
