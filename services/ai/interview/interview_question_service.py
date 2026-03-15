from __future__ import annotations

from typing import Dict, List

from models import CodingChallenge


SUPPORTED_INTERVIEW_ROLES = [
    "Backend Developer",
    "Frontend Developer",
    "AI Engineer",
    "Data Scientist",
    "Full Stack Developer",
]


QUESTION_BANK: Dict[str, List[Dict[str, str]]] = {
    "Backend Developer": [
        {
            "question_text": "Explain REST API principles.",
            "question_type": "technical",
            "expected_answer": "resource-based endpoints,statelessness,http methods,status codes",
            "difficulty": "Beginner",
        },
        {
            "question_text": "What is database indexing and when would you use it?",
            "question_type": "technical",
            "expected_answer": "faster lookups,tradeoff with writes,query performance,search columns",
            "difficulty": "Intermediate",
        },
        {
            "question_text": "Explain ACID properties in databases.",
            "question_type": "technical",
            "expected_answer": "atomicity,consistency,isolation,durability",
            "difficulty": "Intermediate",
        },
        {
            "question_text": "Describe a time you improved reliability in a backend system.",
            "question_type": "behavioral",
            "expected_answer": "problem,action,result,monitoring",
            "difficulty": "Beginner",
        },
    ],
    "Frontend Developer": [
        {
            "question_text": "What is the virtual DOM and why is it useful?",
            "question_type": "technical",
            "expected_answer": "ui diffing,performance,component updates,re-render optimization",
            "difficulty": "Beginner",
        },
        {
            "question_text": "How do you improve web accessibility?",
            "question_type": "technical",
            "expected_answer": "semantic html,keyboard navigation,aria labels,color contrast",
            "difficulty": "Intermediate",
        },
        {
            "question_text": "Explain the difference between state and props.",
            "question_type": "technical",
            "expected_answer": "component data,immutability,parent child flow,re-rendering",
            "difficulty": "Beginner",
        },
        {
            "question_text": "Tell me about a UI bug you solved under pressure.",
            "question_type": "behavioral",
            "expected_answer": "problem,debugging,communication,result",
            "difficulty": "Beginner",
        },
    ],
    "AI Engineer": [
        {
            "question_text": "How do you evaluate a machine learning model?",
            "question_type": "technical",
            "expected_answer": "validation metrics,precision recall,f1,error analysis,baseline comparison",
            "difficulty": "Intermediate",
        },
        {
            "question_text": "What is overfitting and how can you reduce it?",
            "question_type": "technical",
            "expected_answer": "memorizing training data,regularization,cross validation,more data",
            "difficulty": "Beginner",
        },
        {
            "question_text": "Explain the difference between training, validation, and test datasets.",
            "question_type": "technical",
            "expected_answer": "fit model,tune hyperparameters,final evaluation,data split",
            "difficulty": "Beginner",
        },
        {
            "question_text": "Describe a project where you translated AI output into product value.",
            "question_type": "behavioral",
            "expected_answer": "business goal,model choice,measurement,impact",
            "difficulty": "Intermediate",
        },
    ],
    "Data Scientist": [
        {
            "question_text": "How do you handle missing data in a dataset?",
            "question_type": "technical",
            "expected_answer": "imputation,dropping rows,domain knowledge,bias analysis",
            "difficulty": "Beginner",
        },
        {
            "question_text": "What is the bias-variance tradeoff?",
            "question_type": "technical",
            "expected_answer": "underfitting,overfitting,generalization,model complexity",
            "difficulty": "Intermediate",
        },
        {
            "question_text": "When would you use a confusion matrix?",
            "question_type": "technical",
            "expected_answer": "classification,true positives,false positives,false negatives,model analysis",
            "difficulty": "Beginner",
        },
        {
            "question_text": "Tell me about a time you explained data findings to a non-technical audience.",
            "question_type": "behavioral",
            "expected_answer": "communication,insight,decision making,clarity",
            "difficulty": "Beginner",
        },
    ],
    "Full Stack Developer": [
        {
            "question_text": "How do the frontend and backend communicate in a web application?",
            "question_type": "technical",
            "expected_answer": "http requests,apis,json,authentication,error handling",
            "difficulty": "Beginner",
        },
        {
            "question_text": "What are common strategies for securing a full stack application?",
            "question_type": "technical",
            "expected_answer": "authentication,authorization,input validation,https,csrf protection",
            "difficulty": "Intermediate",
        },
        {
            "question_text": "How would you design a scalable course platform?",
            "question_type": "technical",
            "expected_answer": "modular architecture,caching,database design,background jobs,monitoring",
            "difficulty": "Advanced",
        },
        {
            "question_text": "Describe a project where you owned both UI and backend delivery.",
            "question_type": "behavioral",
            "expected_answer": "ownership,tradeoffs,implementation,results",
            "difficulty": "Intermediate",
        },
    ],
}


def _difficulty_rank(value: str) -> int:
    return {"Beginner": 1, "Intermediate": 2, "Advanced": 3}.get(value, 1)


def _coding_interview_question(role: str, difficulty: str, resume_skills: List[str] | None = None) -> Dict[str, str]:
    challenge = (
        CodingChallenge.query
        .filter(CodingChallenge.difficulty == difficulty)
        .order_by(CodingChallenge.created_at.desc(), CodingChallenge.id.desc())
        .first()
    )
    if not challenge:
        challenge = CodingChallenge.query.order_by(CodingChallenge.created_at.desc(), CodingChallenge.id.desc()).first()

    if challenge:
        resume_hint = ""
        if resume_skills:
            resume_hint = f" Highlight experience with {', '.join(resume_skills[:3])} if relevant."
        return {
            "question_text": (
                f"Coding Interview Mode ({difficulty}, 20 minutes): Solve '{challenge.title}' "
                f"for a {role} interview. Explain your approach, complexity, and edge cases.{resume_hint}"
            ),
            "question_type": "coding",
            "expected_answer": f"{challenge.topic},time complexity,space complexity,edge cases,correct approach",
            "difficulty": challenge.difficulty or difficulty,
        }

    return {
        "question_text": (
            f"Coding Interview Mode ({difficulty}, 20 minutes): Describe how you would solve a "
            f"{role} coding problem and explain the algorithm clearly."
        ),
        "question_type": "coding",
        "expected_answer": "approach,time complexity,space complexity,edge cases,test cases",
        "difficulty": difficulty,
    }


def generate_interview_questions(role: str, difficulty: str, resume_skills: List[str] | None = None) -> List[Dict[str, str]]:
    selected_role = role if role in SUPPORTED_INTERVIEW_ROLES else "Full Stack Developer"
    rank = _difficulty_rank(difficulty)
    available = QUESTION_BANK.get(selected_role, QUESTION_BANK["Full Stack Developer"])
    questions = [
        item for item in available
        if _difficulty_rank(item.get("difficulty", "Beginner")) <= rank or item.get("question_type") == "behavioral"
    ]

    technical = [item for item in questions if item["question_type"] == "technical"][:3]
    behavioral = [item for item in questions if item["question_type"] == "behavioral"][:1]
    coding = [_coding_interview_question(selected_role, difficulty, resume_skills=resume_skills)]
    return technical + coding + behavioral
