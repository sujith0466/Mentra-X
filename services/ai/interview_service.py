import random
import re
from typing import List, Dict

# Predefined role-based question bank
QUESTION_BANK = {
    "frontend": [
        {"type": "theory", "question": "What is the virtual DOM in React and why is it faster?", "keywords": ["copy", "diff", "memory", "reconciliation", "update", "render", "state"]},
        {"type": "practical", "question": "Explain how you would optimize a slow-loading React application.", "keywords": ["lazy", "suspense", "memo", "usememo", "usecallback", "minify", "bundle", "code splitting"]},
        {"type": "scenario", "question": "A user complains that a button click sometimes fires twice. How do you debug and fix this?", "keywords": ["debounce", "throttle", "event", "propagation", "state", "disabled", "multiple"]},
        {"type": "theory", "question": "Describe the CSS box model.", "keywords": ["margin", "border", "padding", "content", "box-sizing"]},
        {"type": "practical", "question": "How do you handle state management across deeply nested components?", "keywords": ["context", "redux", "zustand", "prop drilling", "provider"]}
    ],
    "backend": [
        {"type": "theory", "question": "Explain the difference between SQL and NoSQL databases.", "keywords": ["relational", "rigid", "document", "schema", "scale", "acid", "join"]},
        {"type": "practical", "question": "How would you design a rate limiter for an API?", "keywords": ["token bucket", "redis", "ip", "middleware", "sliding window", "cache", "limit"]},
        {"type": "scenario", "question": "Your database queries are running very slowly suddenly. What steps do you take?", "keywords": ["index", "explain", "analyze", "slow query", "lock", "cpu", "connection"]},
        {"type": "theory", "question": "What is REST and what are its key principles?", "keywords": ["stateless", "resource", "http", "methods", "get", "post", "cache", "client-server"]},
        {"type": "practical", "question": "How do you secure a REST API?", "keywords": ["jwt", "oauth", "https", "cors", "rate", "auth", "sanitize"]}
    ],
    "ai": [
        {"type": "theory", "question": "What is the vanishing gradient problem and how is it solved?", "keywords": ["relu", "sigmoid", "deep", "loss", "weight", "backpropagation", "batch normalization", "lstm"]},
        {"type": "practical", "question": "How do you prevent overfitting in a machine learning model?", "keywords": ["regularization", "dropout", "early stopping", "cross-validation", "data augmentation", "l1", "l2"]},
        {"type": "scenario", "question": "Your model has high accuracy on training data but performs poorly in production. What do you do?", "keywords": ["data drift", "overfitting", "distribution", "evaluate", "test set", "generalize", "retrain"]},
        {"type": "theory", "question": "Explain the difference between supervised and unsupervised learning.", "keywords": ["label", "target", "cluster", "classification", "regression", "k-means", "pca"]},
        {"type": "practical", "question": "What evaluation metrics would you choose for an imbalanced classification problem?", "keywords": ["f1", "precision", "recall", "roc", "auc", "confusion matrix"]}
    ],
    "data science": [
        {"type": "theory", "question": "What is the Central Limit Theorem and why is it important?", "keywords": ["distribution", "normal", "sample", "mean", "population", "variance"]},
        {"type": "practical", "question": "How do you handle missing values in a dataset?", "keywords": ["impute", "mean", "median", "drop", "knn", "interpolate", "forward fill"]},
        {"type": "scenario", "question": "A stakeholder asks you to prove that feature X causes metric Y to increase. How do you approach this?", "keywords": ["correlation", "causation", "ab test", "experiment", "control", "treatment", "p-value"]},
        {"type": "theory", "question": "What is the difference between specific types of clustering like K-Means and DBSCAN?", "keywords": ["centroid", "density", "distance", "noise", "outlier", "k", "radius"]},
        {"type": "practical", "question": "Describe the process of feature engineering.", "keywords": ["transform", "encode", "scale", "normalize", "categorical", "one-hot", "extract"]}
    ]
}


def generate_questions(role: str) -> List[Dict]:
    """Generates 3-5 mocked interview questions based on the role."""
    normalized_role = role.strip().lower()
    
    # Map input role to our predetermined keys
    bank_key = "backend"
    if any(k in normalized_role for k in ["front", "web", "ui", "react"]):
        bank_key = "frontend"
    elif any(k in normalized_role for k in ["ai", "machine learning", "ml", "deep"]):
        bank_key = "ai"
    elif any(k in normalized_role for k in ["data", "analyst", "science", "ds"]):
        bank_key = "data science"
    elif "back" in normalized_role or "api" in normalized_role:
        bank_key = "backend"

    questions = QUESTION_BANK.get(bank_key, QUESTION_BANK["backend"])
    
    # Randomly select 3 to 5 questions
    num_questions = min(random.randint(3, 5), len(questions))
    selected = random.sample(questions, num_questions)
    
    return [
        {
            "id": i,
            "type": q["type"],
            "question": q["question"],
            "keywords": q["keywords"]
        }
        for i, q in enumerate(selected)
    ]

def evaluate_answer(question_data: dict, user_answer: str) -> dict:
    """Evaluates the user's answer against the question's expected keywords to produce a score and feedback."""
    answer = str(user_answer or "").lower().strip()
    if not answer:
         return {
            "score": 0,
            "feedback": "You did not provide an answer.",
            "improvement": "Always attempt to provide at least a partial explanation, even if unsure."
         }

    keywords = question_data.get("keywords", [])
    if not keywords:
         # Fallback if no keywords were defined
         return {
            "score": 5,
            "feedback": "A simple answer was provided, but more depth is needed.",
            "improvement": "Try to expand on the core concepts."
         }

    # Clean the input answer heavily for matching
    cleaned_answer = re.sub(r'[^\w\s]', '', answer)
    words_in_answer = set(cleaned_answer.split())
    
    matches = 0
    matched_keywords = []
    missing_keywords = []

    for kw in keywords:
        # Check if keyword is part of any word or substring in the original answer
        if kw in answer:
             matches += 1
             matched_keywords.append(kw)
        else:
             missing_keywords.append(kw)
             
    # Calculate score base on ratio of matched keywords
    # A great answer doesn't need ALL keywords, hitting ~40% might be a 10/10 for simple rule-sets.
    ratio = matches / len(keywords) if len(keywords) > 0 else 0
    
    # Scale: ratio >= 0.4 -> 10. ratio = 0 -> 2 (for trying)
    calc_score = round(min(10, max(1, (ratio / 0.4) * 10)))
    
    # Construct feedback
    if calc_score >= 8:
        feedback = f"Excellent answer! You correctly covered key concepts like: {', '.join(matched_keywords[:3])}."
        improvement = "Try providing a real-world example to make your answer even stronger." if len(answer) < 50 else "Keep up the great depth."
    elif calc_score >= 5:
        feedback = f"Good attempt. You mentioned some relevant points like {', '.join(matched_keywords[:2]) if matched_keywords else 'basic mechanisms'}."
        improvement = f"To improve, make sure to discuss concepts such as: {', '.join(missing_keywords[:2])}."
    else:
        feedback = "Your answer missed several core technical details expected for this topic."
        improvement = f"Review the foundational concepts. Specifically, look into: {', '.join(missing_keywords[:3])}."
        
    return {
        "score": calc_score,
        "feedback": feedback,
        "improvement": improvement
    }
