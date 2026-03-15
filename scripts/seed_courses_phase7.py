from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app import app
from models import Assignment, Course, CourseModule, Domain, Quiz, QuizQuestion, Syllabus, Video, db


DOMAIN_VIDEO_URLS = {
    "Web Development": [
        "https://www.youtube.com/embed/mU6anWqZJcc",
        "https://www.youtube.com/embed/UB1O30fR-EE",
        "https://www.youtube.com/embed/PkZNo7MFNFg",
        "https://www.youtube.com/embed/jBzwzrDvZ18",
    ],
    "Artificial Intelligence": [
        "https://www.youtube.com/embed/aircAruvnKk",
        "https://www.youtube.com/embed/JMUxmLyrhSk",
        "https://www.youtube.com/embed/2ePf9rue1Ao",
        "https://www.youtube.com/embed/5NgNicANyqM",
    ],
    "Data Science": [
        "https://www.youtube.com/embed/r-uOLxNrNk8",
        "https://www.youtube.com/embed/vmEHCJofslg",
        "https://www.youtube.com/embed/GPVsHOlRBBI",
        "https://www.youtube.com/embed/LHBE6Q9XlzI",
    ],
    "Machine Learning": [
        "https://www.youtube.com/embed/GwIo3gDZCVQ",
        "https://www.youtube.com/embed/ukzFI9rgwfU",
        "https://www.youtube.com/embed/4b5d3muPQmA",
        "https://www.youtube.com/embed/i_LwzRVP7bg",
    ],
    "Cybersecurity": [
        "https://www.youtube.com/embed/inWWhr5tnEA",
        "https://www.youtube.com/embed/3Kq1MIfTWCE",
        "https://www.youtube.com/embed/U_P23SqJaDc",
        "https://www.youtube.com/embed/0k2EJXwXUmE",
    ],
    "Cloud Computing": [
        "https://www.youtube.com/embed/2LaAJq1lB1Q",
        "https://www.youtube.com/embed/kTp5xUtcalw",
        "https://www.youtube.com/embed/fqMOX6JJhGo",
        "https://www.youtube.com/embed/X48VuDVv0do",
    ],
    "DevOps": [
        "https://www.youtube.com/embed/0yWAtQ6wYNM",
        "https://www.youtube.com/embed/1hHMwLxN6EM",
        "https://www.youtube.com/embed/scEDHsr3APg",
        "https://www.youtube.com/embed/lAn7GhaEFN8",
    ],
    "Mobile Development": [
        "https://www.youtube.com/embed/F9UC9DY-vIU",
        "https://www.youtube.com/embed/x0uinJvhNxI",
        "https://www.youtube.com/embed/VPvVD8t02U8",
        "https://www.youtube.com/embed/1gDhl4leEzA",
    ],
    "Blockchain": [
        "https://www.youtube.com/embed/SSo_EIwHSd4",
        "https://www.youtube.com/embed/M576WGiDBdQ",
        "https://www.youtube.com/embed/gyMwXuJrbJQ",
        "https://www.youtube.com/embed/8jI1TuEaTro",
    ],
    "Software Engineering": [
        "https://www.youtube.com/embed/QMbx0dTWJIQ",
        "https://www.youtube.com/embed/UzLMhqg3_Wc",
        "https://www.youtube.com/embed/FLtqAi7WNBY",
        "https://www.youtube.com/embed/9GDX-IyZ_C8",
    ],
}

DOMAIN_MODULES = {
    "Web Development": [
        "Foundations of the Web",
        "Page Structure and Styling",
        "Interactive Frontend Development",
        "Backend Integration",
        "Testing and Deployment",
        "Final Project",
    ],
    "Artificial Intelligence": [
        "AI Foundations",
        "Problem Solving with Python",
        "Intelligent Systems and Models",
        "Real World AI Applications",
        "Ethics and Evaluation",
        "Final Project",
    ],
    "Data Science": [
        "Data Science Foundations",
        "Working with Data",
        "Visualization and Storytelling",
        "Statistical Reasoning",
        "Insights and Decision Making",
        "Final Project",
    ],
    "Machine Learning": [
        "ML Foundations",
        "Preparing Data",
        "Training Models",
        "Evaluation and Improvement",
        "Deployment Thinking",
        "Final Project",
    ],
    "Cybersecurity": [
        "Security Foundations",
        "Threats and Risk Awareness",
        "Network and Application Security",
        "Detection and Response",
        "Hardening Best Practices",
        "Final Project",
    ],
    "Cloud Computing": [
        "Cloud Foundations",
        "Core Services and Architecture",
        "Containers and Compute",
        "Scaling and Reliability",
        "Security and Cost Control",
        "Final Project",
    ],
    "DevOps": [
        "DevOps Culture and Workflow",
        "Source Control and Automation",
        "CI/CD Delivery Practices",
        "Infrastructure and Environments",
        "Monitoring and Reliability",
        "Final Project",
    ],
    "Mobile Development": [
        "Mobile Foundations",
        "UI and Navigation",
        "State and Data Handling",
        "Platform Features",
        "Testing and Release",
        "Final Project",
    ],
    "Blockchain": [
        "Blockchain Foundations",
        "Transactions and Consensus",
        "Smart Contract Development",
        "Security and Testing",
        "DApp Integration",
        "Final Project",
    ],
    "Software Engineering": [
        "Engineering Foundations",
        "Requirements and Design",
        "Architecture and Patterns",
        "Testing and Quality",
        "Collaboration and Delivery",
        "Final Project",
    ],
}

CATALOG = {
    "Web Development": [
        ("HTML & CSS Fundamentals", "Master semantic HTML, responsive CSS, and layout systems.", "Build a multi-page responsive landing site", "Mentra Web Team"),
        ("JavaScript for Beginners", "Learn JavaScript syntax, DOM interactions, and beginner-friendly logic.", "Build an interactive study planner widget", "Mentra Web Team"),
        ("React.js Frontend Development", "Create reusable components and interactive frontend applications with React.", "Build a task management dashboard in React", "Mentra Frontend Lab"),
        ("Backend Development with Flask", "Build Python-powered web backends, routing layers, and APIs using Flask.", "Build a REST API for a blog platform", "Mentra Backend Lab"),
        ("Full Stack Web Development", "Connect frontend and backend systems to build complete web products.", "Build a full-stack course marketplace", "Mentra Full Stack Studio"),
    ],
    "Artificial Intelligence": [
        ("Introduction to Artificial Intelligence", "Explore the core ideas behind intelligent systems and real-world AI usage.", "Build a rule-based AI assistant prototype", "Mentra AI Faculty"),
        ("AI Applications with Python", "Use Python to solve practical AI-style automation and reasoning tasks.", "Build a Python-based AI automation workflow", "Mentra AI Faculty"),
        ("Deep Learning Fundamentals", "Understand neural networks, deep learning workflow, and model behavior.", "Build a neural network demo for image patterns", "Mentra Deep Learning Lab"),
        ("Computer Vision Basics", "Learn image-based AI concepts for detection, classification, and visual reasoning.", "Build an image classification demo", "Mentra Vision Lab"),
        ("Natural Language Processing", "Work with language data, text pipelines, and NLP applications.", "Build a text classification assistant", "Mentra NLP Lab"),
    ],
    "Data Science": [
        ("Data Science with Python", "Apply Python tools for cleaning, exploring, and analyzing data.", "Build a student performance analysis notebook", "Mentra Data Team"),
        ("Data Analysis with Pandas", "Use Pandas for data wrangling, filtering, aggregation, and reporting.", "Build a business KPI analysis script", "Mentra Data Team"),
        ("Data Visualization with Matplotlib", "Create analytical charts and communicate findings clearly.", "Build a dashboard-ready visualization package", "Mentra Visualization Lab"),
        ("Statistics for Data Science", "Learn the statistical concepts needed to reason about data confidently.", "Build a data insight report with hypothesis checks", "Mentra Analytics Lab"),
    ],
    "Machine Learning": [
        ("Machine Learning Fundamentals", "Learn supervised and unsupervised learning at a practical level.", "Train a basic prediction model using a real dataset", "Mentra ML Team"),
        ("Supervised Learning", "Build predictive models using labeled data and common supervised techniques.", "Build a classification pipeline for tabular data", "Mentra ML Team"),
        ("Unsupervised Learning", "Discover patterns, clusters, and structure without labeled targets.", "Build a customer segmentation prototype", "Mentra ML Team"),
        ("Model Evaluation Techniques", "Evaluate models using metrics, validation patterns, and error analysis.", "Build a model comparison report", "Mentra ML Team"),
    ],
    "Cybersecurity": [
        ("Introduction to Cybersecurity", "Understand the threat landscape, risk, and core security practices.", "Create a basic security awareness toolkit", "Mentra Security Team"),
        ("Ethical Hacking Basics", "Learn safe security testing concepts and introductory attack simulation ideas.", "Build a web security checklist and audit report", "Mentra Security Team"),
        ("Network Security", "Protect networked systems with secure architecture and layered defenses.", "Design a secure office network blueprint", "Mentra Security Team"),
        ("Web Application Security", "Protect web apps from common vulnerabilities and insecure patterns.", "Audit and harden a sample web application", "Mentra Security Team"),
    ],
    "Cloud Computing": [
        ("Cloud Computing Fundamentals", "Learn cloud concepts, service models, and distributed architecture basics.", "Design a cloud-ready architecture for a student platform", "Mentra Cloud Team"),
        ("AWS Basics", "Get started with AWS services and foundational cloud workflows.", "Deploy a starter application architecture on AWS", "Mentra Cloud Team"),
        ("Docker & Containers", "Package applications reliably with containers and image-based workflows.", "Containerize a Flask learning app", "Mentra Cloud Team"),
        ("Kubernetes Introduction", "Understand orchestration, scaling, and deployment management with Kubernetes.", "Design a Kubernetes deployment plan for a web service", "Mentra Cloud Team"),
    ],
    "DevOps": [
        ("DevOps Fundamentals", "Understand DevOps culture, automation, feedback loops, and collaboration.", "Design a DevOps workflow for a student product team", "Mentra DevOps Guild"),
        ("CI/CD Pipelines", "Build continuous integration and delivery workflows that improve release quality.", "Build a CI/CD pipeline for a Flask app", "Mentra DevOps Guild"),
        ("Infrastructure as Code", "Manage infrastructure through code-driven provisioning and repeatable automation.", "Create infrastructure templates for a cloud app", "Mentra DevOps Guild"),
        ("Monitoring & Logging", "Use telemetry, logging, and alerting to improve service reliability.", "Build an operational observability plan", "Mentra DevOps Guild"),
    ],
    "Mobile Development": [
        ("Android Development with Kotlin", "Build Android apps using Kotlin fundamentals and platform patterns.", "Build an Android note-taking app", "Mentra Mobile Team"),
        ("Flutter Mobile Development", "Create cross-platform mobile apps using Flutter widgets and state flows.", "Build a Flutter learning tracker app", "Mentra Mobile Team"),
        ("React Native Basics", "Use React Native to build mobile interfaces with JavaScript skills.", "Build a React Native task planner", "Mentra Mobile Team"),
    ],
    "Blockchain": [
        ("Blockchain Fundamentals", "Understand distributed ledgers, transactions, and blockchain architecture.", "Explain and prototype a blockchain transaction explorer", "Mentra Blockchain Lab"),
        ("Smart Contracts with Solidity", "Learn smart contract basics, Solidity syntax, and deployment thinking.", "Build and test a simple voting smart contract", "Mentra Blockchain Lab"),
    ],
    "Software Engineering": [
        ("Software Engineering Principles", "Learn maintainable software practices, process, and quality fundamentals.", "Design a maintainable LMS feature specification", "Mentra Engineering Guild"),
        ("System Design Fundamentals", "Understand scalable system design concepts and tradeoff analysis.", "Design the architecture for a course streaming platform", "Mentra Engineering Guild"),
        ("Agile Product Development", "Collaborate across planning, delivery, feedback, and iteration cycles.", "Create a sprint-driven roadmap for an education app", "Mentra Engineering Guild"),
    ],
}


def ensure_domain(name: str) -> tuple[Domain, bool]:
    domain = Domain.query.filter_by(name=name).first()
    if domain:
        return domain, False
    domain = Domain(name=name, description=f"Structured learning paths for {name}.")
    db.session.add(domain)
    db.session.flush()
    return domain, True


def ensure_course(domain: Domain, title: str, description: str, project_title: str, instructor: str) -> tuple[Course, bool]:
    course = Course.query.filter_by(title=title).first()
    created = False
    if not course:
        course = Course(title=title, domain_id=domain.id)
        db.session.add(course)
        db.session.flush()
        created = True
    course.description = description
    course.domain_id = domain.id
    course.price = 0.0
    course.instructor = instructor
    course.status = "published"
    course.demo_video_url = DOMAIN_VIDEO_URLS[domain.name][0]
    if not course.image_url:
        course.image_url = ""
    return course, created


def ensure_syllabus(course: Course, module_titles: list[str]) -> int:
    created = 0
    for order, title in enumerate(module_titles, start=1):
        exists = Syllabus.query.filter_by(course_id=course.id, topic_title=title).first()
        if exists:
            exists.order_number = order
            exists.topic_description = f"Key learning outcomes and practical coverage for {title.lower()}."
            continue
        db.session.add(Syllabus(
            course_id=course.id,
            topic_title=title,
            topic_description=f"Key learning outcomes and practical coverage for {title.lower()}.",
            order_number=order,
        ))
        created += 1
    return created


def lesson_titles(module_title: str, is_final_project: bool) -> list[str]:
    if is_final_project:
        return [
            f"Project Brief for {module_title}",
            f"Planning the {module_title}",
            f"Building the {module_title}",
            f"Presenting the {module_title}",
        ]
    return [
        f"Introduction to {module_title}",
        f"Core Concepts in {module_title}",
        f"Hands-on Lab for {module_title}",
        f"Best Practices in {module_title}",
    ]


def ensure_module_content(course: Course, domain_name: str, module_title: str, module_order: int, project_title: str) -> dict[str, int]:
    counts = {"modules": 0, "videos": 0, "quizzes": 0, "questions": 0, "assignments": 0}
    module = CourseModule.query.filter_by(course_id=course.id, title=module_title).first()
    if not module:
        module = CourseModule(course_id=course.id, title=module_title, order_index=module_order)
        db.session.add(module)
        db.session.flush()
        counts["modules"] += 1
    else:
        module.order_index = module_order

    video_urls = DOMAIN_VIDEO_URLS[domain_name]
    is_final_project = module_title == "Final Project"
    titles = lesson_titles(module_title if not is_final_project else project_title, is_final_project)

    for lesson_order, title in enumerate(titles, start=1):
        lesson = Video.query.filter_by(course_id=course.id, module_id=module.id, title=title).first()
        if not lesson:
            lesson = Video(course_id=course.id, module_id=module.id, title=title, video_url=video_urls[(lesson_order - 1) % len(video_urls)])
            db.session.add(lesson)
            counts["videos"] += 1
        lesson.description = f"Guided instruction for {title.lower()} in the course {course.title}."
        lesson.duration = ["08:30", "10:45", "12:15", "09:50"][(lesson_order - 1) % 4]
        lesson.video_url = video_urls[(lesson_order - 1) % len(video_urls)]
        lesson.order_number = lesson_order

    quiz_title = f"{module_title} Quiz"
    quiz = Quiz.query.filter_by(course_id=course.id, module_id=module.id, title=quiz_title).first()
    if not quiz:
        quiz = Quiz(
            course_id=course.id,
            module_id=module.id,
            title=quiz_title,
            description=f"Checkpoint quiz for {module_title.lower()}.",
            question_count_target=4,
            passing_percentage=60.0,
            time_limit_minutes=12,
            attempts_allowed=3,
            is_enabled=True,
        )
        db.session.add(quiz)
        db.session.flush()
        counts["quizzes"] += 1
    else:
        quiz.description = f"Checkpoint quiz for {module_title.lower()}."

    questions = [
        {
            "question_text": f"What is a core goal of {module_title}?",
            "question_type": "mcq",
            "option_a": "Applying practical concepts in a structured way",
            "option_b": "Avoiding all hands-on work",
            "option_c": "Skipping the module entirely",
            "option_d": "Memorizing without practice",
            "correct_answer": "Applying practical concepts in a structured way",
        },
        {
            "question_text": f"True or False: {module_title} is part of the course {course.title}.",
            "question_type": "true_false",
            "option_a": "True",
            "option_b": "False",
            "option_c": None,
            "option_d": None,
            "correct_answer": "True",
        },
        {
            "question_text": f"Which approach best supports success in {module_title}?",
            "question_type": "mcq",
            "option_a": "Practice, review, and iterative improvement",
            "option_b": "Ignoring feedback",
            "option_c": "Skipping exercises",
            "option_d": "Only reading titles",
            "correct_answer": "Practice, review, and iterative improvement",
        },
        {
            "question_text": f"True or False: Hands-on tasks are unnecessary in {module_title}.",
            "question_type": "true_false",
            "option_a": "True",
            "option_b": "False",
            "option_c": None,
            "option_d": None,
            "correct_answer": "False",
        },
    ]

    for index, payload in enumerate(questions, start=1):
        question = QuizQuestion.query.filter_by(quiz_id=quiz.id, question_text=payload["question_text"]).first()
        if not question:
            question = QuizQuestion(quiz_id=quiz.id, question_text=payload["question_text"])
            db.session.add(question)
            counts["questions"] += 1
        question.question_type = payload["question_type"]
        question.option_a = payload["option_a"]
        question.option_b = payload["option_b"]
        question.option_c = payload["option_c"]
        question.option_d = payload["option_d"]
        question.correct_answer = payload["correct_answer"]
        question.order_index = index
        question.order_number = index

    if module_title == "Final Project":
        assignment_title = f"Final Project: {project_title}"
        instructions = (
            f"Build and submit the final course project for {course.title}. "
            f"Deliver a working solution, short documentation, and a reflection on decisions made while building {project_title.lower()}."
        )
        marks = 100.0
    else:
        assignment_title = f"{module_title} Practical Assignment"
        instructions = (
            f"Complete a practical task for {module_title.lower()} in {course.title}. "
            f"Show your process, implementation steps, and final outcome."
        )
        marks = 40.0

    assignment = Assignment.query.filter_by(course_id=course.id, module_id=module.id, title=assignment_title).first()
    if not assignment:
        assignment = Assignment(course_id=course.id, module_id=module.id, title=assignment_title, instructions=instructions, marks=marks)
        db.session.add(assignment)
        counts["assignments"] += 1
    else:
        assignment.instructions = instructions
        assignment.marks = marks

    return counts


def seed_catalog() -> dict[str, int]:
    totals = {
        "domains_created": 0,
        "courses_created": 0,
        "modules_created": 0,
        "syllabus_created": 0,
        "videos_created": 0,
        "quizzes_created": 0,
        "questions_created": 0,
        "assignments_created": 0,
        "courses_total": 0,
    }

    for domain_name, courses in CATALOG.items():
        domain, domain_created = ensure_domain(domain_name)
        totals["domains_created"] += 1 if domain_created else 0
        module_titles = DOMAIN_MODULES[domain_name]

        for title, description, project_title, instructor in courses:
            course, course_created = ensure_course(domain, title, description, project_title, instructor)
            totals["courses_created"] += 1 if course_created else 0
            totals["courses_total"] += 1
            totals["syllabus_created"] += ensure_syllabus(course, module_titles)

            for module_order, module_title in enumerate(module_titles, start=1):
                counts = ensure_module_content(course, domain_name, module_title, module_order, project_title)
                for key, value in counts.items():
                    totals[f"{key}_created"] += value

    db.session.commit()
    return totals


def main() -> None:
    with app.app_context():
        totals = seed_catalog()
        print("Phase-7 course ecosystem seeding completed")
        print(f"Domains ensured: {len(CATALOG)}")
        print(f"Courses ensured: {totals['courses_total']}")
        print(f"New domains created: {totals['domains_created']}")
        print(f"New courses created: {totals['courses_created']}")
        print(f"New modules created: {totals['modules_created']}")
        print(f"New syllabus topics created: {totals['syllabus_created']}")
        print(f"New lesson videos created: {totals['videos_created']}")
        print(f"New quizzes created: {totals['quizzes_created']}")
        print(f"New quiz questions created: {totals['questions_created']}")
        print(f"New assignments created: {totals['assignments_created']}")


if __name__ == "__main__":
    main()
