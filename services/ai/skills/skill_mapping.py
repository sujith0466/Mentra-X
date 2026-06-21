from __future__ import annotations

from typing import Dict, List


COURSE_SKILL_MAP: Dict[str, List[str]] = {
    "Python Programming": ["Python Basics", "Variables", "Functions", "OOP"],
    "Python Programming - Beginner to Advanced": ["Python Basics", "Variables", "Functions", "OOP"],
    "Backend Development with Flask": ["Flask Routing", "REST APIs", "Authentication", "Flask Architecture"],
    "Flask Web Development": ["Flask Routing", "REST APIs", "Authentication", "Flask Architecture"],
    "Full Stack Web Development": ["Frontend Integration", "REST APIs", "Authentication", "Deployment Basics"],
    "HTML & CSS Fundamentals": ["HTML Structure", "CSS Styling", "Responsive Layouts", "Accessibility Basics"],
    "JavaScript for Beginners": ["JavaScript Basics", "DOM Manipulation", "Functions", "Control Flow"],
    "React.js Frontend Development": ["React Components", "State Management", "Frontend Routing", "Reusable UI Patterns"],
    "React Frontend Development": ["React Components", "State Management", "Frontend Routing", "Reusable UI Patterns"],
    "Introduction to Artificial Intelligence": ["AI Foundations", "Problem Solving", "Model Thinking", "Ethical AI"],
    "AI Applications with Python": ["Python Automation", "AI Workflows", "Data Processing", "Applied AI"],
    "Deep Learning Fundamentals": ["Neural Networks", "Deep Learning", "Model Training", "Evaluation"],
    "Computer Vision Basics": ["Image Processing", "Computer Vision", "Classification", "Model Evaluation"],
    "Natural Language Processing": ["Text Processing", "NLP", "Tokenization", "Language Models"],
    "Data Science with Python": ["Data Cleaning", "Python Analysis", "Feature Exploration", "Reporting"],
    "Data Analysis with Pandas": ["Pandas", "Data Wrangling", "Aggregation", "Tabular Analysis"],
    "Data Visualization with Matplotlib": ["Visualization", "Chart Design", "Storytelling", "Insight Communication"],
    "Statistics for Data Science": ["Statistics", "Probability", "Hypothesis Testing", "Inference"],
    "Machine Learning Fundamentals": ["Supervised Learning", "Regression", "Classification", "Model Evaluation"],
    "Supervised Learning": ["Regression", "Classification", "Training Data", "Prediction"],
    "Unsupervised Learning": ["Clustering", "Dimensionality Reduction", "Pattern Discovery", "Segmentation"],
    "Model Evaluation Techniques": ["Validation", "Metrics", "Error Analysis", "Model Comparison"],
    "Introduction to Cybersecurity": ["Security Foundations", "Threat Awareness", "Risk Management", "Access Control"],
    "Ethical Hacking Basics": ["Reconnaissance", "Web Testing", "Security Auditing", "Responsible Disclosure"],
    "Network Security": ["Network Defense", "Traffic Analysis", "Firewalls", "Secure Architecture"],
    "Web Application Security": ["OWASP Risks", "Input Validation", "Authentication Security", "Hardening"],
    "Cloud Computing Fundamentals": ["Cloud Concepts", "Service Models", "Scalability", "Availability"],
    "AWS Basics": ["AWS Services", "Cloud Deployment", "Identity Basics", "Storage"],
    "Docker & Containers": ["Containers", "Images", "Environment Isolation", "Container Workflows"],
    "Kubernetes Introduction": ["Orchestration", "Pods and Services", "Scaling", "Deployment Management"],
    "DevOps Fundamentals": ["Automation", "Collaboration", "Delivery Workflow", "Release Practices"],
    "CI/CD Pipelines": ["Continuous Integration", "Continuous Delivery", "Build Automation", "Release Gates"],
    "Infrastructure as Code": ["Infrastructure Templates", "Provisioning", "Environment Consistency", "Automation"],
    "Monitoring & Logging": ["Observability", "Logging", "Alerting", "Reliability"],
    "Android Development with Kotlin": ["Kotlin Basics", "Android UI", "State Handling", "Mobile Navigation"],
    "Flutter Mobile Development": ["Flutter Widgets", "Cross Platform UI", "State Management", "Mobile Deployment"],
    "React Native Basics": ["React Native", "Mobile Components", "Navigation", "State Management"],
    "Blockchain Fundamentals": ["Distributed Ledgers", "Transactions", "Consensus", "Blockchain Architecture"],
    "Smart Contracts with Solidity": ["Solidity", "Smart Contracts", "Contract Testing", "Blockchain Security"],
    "Software Engineering Principles": ["Requirements", "Code Quality", "Maintainability", "Engineering Workflow"],
    "System Design Fundamentals": ["Scalability", "Architecture", "Tradeoffs", "Distributed Systems"],
    "Agile Product Development": ["Agile Delivery", "Sprint Planning", "Feedback Loops", "Product Iteration"],
}


def infer_skills_for_course(course_title: str, module_titles: List[str] | None = None) -> List[str]:
    title = (course_title or "").strip()
    if title in COURSE_SKILL_MAP:
        return COURSE_SKILL_MAP[title]

    inferred: List[str] = []
    for module_title in module_titles or []:
        cleaned = (module_title or "").replace("Final Project", "Project Delivery").strip()
        if cleaned and cleaned not in inferred:
            inferred.append(cleaned)
    if inferred:
        return inferred[:4]

    fallback_words = [segment.strip().title() for segment in title.replace("with", " ").replace("&", " ").split() if len(segment.strip()) > 3]
    return list(dict.fromkeys(fallback_words[:4])) or ["Core Foundations"]
