"""Safe Mentra catalog restoration script.

- Preserves existing data
- Adds only missing curated courses
- Publishes curated courses
- Adds modules, lessons, and basic syllabus when missing
"""

from backend.app import app, db
from backend.models import Course, Domain, CourseModule, Video, Syllabus
from sqlalchemy import func

VIDEO_URLS = [
    "https://www.youtube.com/watch?v=rfscVS0vtbw",
    "https://www.youtube.com/watch?v=9bZkp7q19f0",
    "https://www.youtube.com/watch?v=ysz5S6PUM-U",
    "https://www.youtube.com/watch?v=aqz-KE-bpKQ",
    "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
]

IMAGE_BY_KEYWORD = {
    "python": "python_for_datascience.jpg",
    "data": "data_analytics_powerbi.png",
    "machine": "machine_learning.jpg",
    "deep": "deep_learning.jpeg",
    "flask": "flask_fullstack.jpg",
    "django": "flask_fullstack.jpg",
    "react native": "react_native.png",
    "react": "react_js.png",
    "node": "mern_stack.jpg",
    "javascript": "react_js.png",
    "docker": "docker_kubernetes.png",
    "kubernetes": "docker_kubernetes.png",
    "linux": "network_security.jpg",
    "git": "nextjs.jpg",
    "api": "nextjs.jpg",
    "sql": "data_analytics_powerbi.png",
    "mongodb": "mern_stack.jpg",
    "aws": "aws.png",
    "cyber": "network_security.jpg",
    "ethical": "ethical_hacking.png",
    "flutter": "flutter.png",
    "ui/ux": "nextjs.jpg",
    "system design": "aws.png",
    "algorithm": "machine_learning.jpg",
    "nlp": "nlp.jpg",
    "vision": "deep_learning.jpeg",
}

NOISE_PATTERNS = (
    "phase2 temp",
    "phase2 empty",
    "stability ",
    "temp course",
    "test course",
)

CATALOG = [
    {
        "title": "Python Programming - Beginner to Advanced",
        "description": "Build strong Python foundations and practical project skills from basics to advanced concepts.",
        "instructor": "Ananya Rao",
        "domain": "Software Engineering",
        "track": "python",
    },
    {
        "title": "Data Science with Python",
        "description": "Learn data analysis, visualization, and machine learning workflows using Python and industry tools.",
        "instructor": "Rahul Menon",
        "domain": "Data Science",
        "track": "data",
    },
    {
        "title": "Machine Learning Fundamentals",
        "description": "Master supervised and unsupervised learning with practical datasets and model evaluation.",
        "instructor": "Priya Sharma",
        "domain": "Data Science",
        "track": "ml",
    },
    {
        "title": "Deep Learning with PyTorch",
        "description": "Train neural networks with PyTorch, from tensors and backpropagation to deployment basics.",
        "instructor": "Karan Verma",
        "domain": "Artificial Intelligence",
        "track": "dl",
    },
    {
        "title": "Flask Web Development",
        "description": "Build production-ready Flask applications with routing, templates, forms, and APIs.",
        "instructor": "Meera Iyer",
        "domain": "Web Development",
        "track": "web",
    },
    {
        "title": "Django Full Stack Development",
        "description": "Develop complete Django web apps with authentication, ORM, and scalable architecture.",
        "instructor": "Arjun Nair",
        "domain": "Web Development",
        "track": "web",
    },
    {
        "title": "React Frontend Development",
        "description": "Create modern, responsive frontends with React, component design, and state handling.",
        "instructor": "Neha Kapoor",
        "domain": "Web Development",
        "track": "frontend",
    },
    {
        "title": "Node.js Backend Development",
        "description": "Design robust backend services with Node.js, Express, middleware, and API security.",
        "instructor": "Siddharth Jain",
        "domain": "Web Development",
        "track": "backend",
    },
    {
        "title": "Modern JavaScript ES6+",
        "description": "Master core and advanced JavaScript features used in modern frontend and backend stacks.",
        "instructor": "Ritika Sen",
        "domain": "Web Development",
        "track": "frontend",
    },
    {
        "title": "Docker & Kubernetes DevOps",
        "description": "Containerize, orchestrate, and deploy applications with Docker and Kubernetes workflows.",
        "instructor": "Dev Malik",
        "domain": "Cloud Computing",
        "track": "devops",
    },
    {
        "title": "Linux for Developers",
        "description": "Use Linux confidently for development, shell automation, process control, and deployment.",
        "instructor": "Vikram Kulkarni",
        "domain": "Software Engineering",
        "track": "devops",
    },
    {
        "title": "Git & GitHub Mastery",
        "description": "Learn practical version control, branching strategies, pull requests, and team workflows.",
        "instructor": "Aditi Das",
        "domain": "Software Engineering",
        "track": "se",
    },
    {
        "title": "REST API Development",
        "description": "Design clean REST APIs with authentication, validation, pagination, and testing.",
        "instructor": "Manish Gupta",
        "domain": "Web Development",
        "track": "backend",
    },
    {
        "title": "SQL & Database Design",
        "description": "Understand schema design, normalization, indexing, and SQL query optimization.",
        "instructor": "Sonal Arora",
        "domain": "Data Science",
        "track": "data",
    },
    {
        "title": "MongoDB for Developers",
        "description": "Work with document databases, aggregation pipelines, and scalable schema design in MongoDB.",
        "instructor": "Kabir Sethi",
        "domain": "Web Development",
        "track": "backend",
    },
    {
        "title": "AWS Cloud Fundamentals",
        "description": "Get hands-on with core AWS services, IAM, compute, storage, and cloud architecture basics.",
        "instructor": "Nisha Pillai",
        "domain": "Cloud Computing",
        "track": "cloud",
    },
    {
        "title": "Cybersecurity Basics",
        "description": "Learn security principles, attack surfaces, risk reduction, and secure engineering basics.",
        "instructor": "Aman Roy",
        "domain": "Cyber Security",
        "track": "security",
    },
    {
        "title": "Ethical Hacking Fundamentals",
        "description": "Understand penetration testing phases, reconnaissance, and reporting using ethical practices.",
        "instructor": "Kriti Bansal",
        "domain": "Cyber Security",
        "track": "security",
    },
    {
        "title": "Flutter Mobile Development",
        "description": "Build cross-platform mobile apps with Flutter widgets, state management, and deployment.",
        "instructor": "Pooja Arvind",
        "domain": "Mobile App Development",
        "track": "mobile",
    },
    {
        "title": "React Native Mobile Apps",
        "description": "Develop native-like mobile apps with React Native and reusable JavaScript components.",
        "instructor": "Nitin Yadav",
        "domain": "Mobile App Development",
        "track": "mobile",
    },
    {
        "title": "UI/UX Design Fundamentals",
        "description": "Learn user-centered design, wireframes, prototypes, and usability evaluation techniques.",
        "instructor": "Maya Fernandes",
        "domain": "Web Development",
        "track": "design",
    },
    {
        "title": "Software Engineering Principles",
        "description": "Apply software engineering best practices: architecture, testing, maintainability, and delivery.",
        "instructor": "Rohan Bhatt",
        "domain": "Software Engineering",
        "track": "se",
    },
    {
        "title": "System Design for Developers",
        "description": "Design scalable systems with distributed architecture, caching, queues, and reliability patterns.",
        "instructor": "Ishita Chandra",
        "domain": "Software Engineering",
        "track": "se",
    },
    {
        "title": "Data Structures & Algorithms",
        "description": "Strengthen problem solving with core data structures, algorithms, and complexity analysis.",
        "instructor": "Aditya Kumar",
        "domain": "Software Engineering",
        "track": "dsa",
    },
    {
        "title": "AI Fundamentals",
        "description": "Build foundational knowledge of AI concepts, workflows, model development, and ethical considerations.",
        "instructor": "Sneha Murthy",
        "domain": "Artificial Intelligence",
        "track": "ai",
    },
    {
        "title": "Natural Language Processing",
        "description": "Process and model language data with tokenization, embeddings, transformers, and evaluation.",
        "instructor": "Tanvi Joshi",
        "domain": "Artificial Intelligence",
        "track": "nlp",
    },
    {
        "title": "Computer Vision Basics",
        "description": "Work with image preprocessing, feature extraction, CNN fundamentals, and vision applications.",
        "instructor": "Harsh Dubey",
        "domain": "Artificial Intelligence",
        "track": "cv",
    },
]

MODULE_TEMPLATES = {
    "python": [
        ("Python Basics", ["Introduction to Python", "Installing Python", "Variables and Data Types", "Operators and Expressions"]),
        ("Control Flow & Functions", ["If and Else", "Loops in Python", "Functions and Scope", "Error Handling Basics"]),
        ("Data Structures", ["Lists and Tuples", "Dictionaries", "Sets", "Comprehensions"]),
        ("Practical Projects", ["File Handling Project", "CLI Utility", "Mini Automation Script", "Final Capstone"]),
    ],
    "data": [
        ("Data Foundations", ["Data Lifecycle", "Python for Data Work", "NumPy Essentials", "Pandas Basics"]),
        ("Data Analysis", ["Data Cleaning", "Exploratory Analysis", "Feature Engineering", "Statistical Summaries"]),
        ("Visualization", ["Matplotlib Basics", "Seaborn Charts", "Dashboard Thinking", "Storytelling with Data"]),
        ("Applied Workflow", ["End-to-End Dataset Project", "Modeling Readiness", "Presentation of Insights", "Portfolio Packaging"]),
    ],
    "ml": [
        ("ML Foundations", ["What is Machine Learning", "Train/Test Split", "Evaluation Metrics", "Bias and Variance"]),
        ("Supervised Learning", ["Linear Models", "Tree-Based Models", "Ensemble Methods", "Model Comparison"]),
        ("Unsupervised Learning", ["Clustering", "Dimensionality Reduction", "Anomaly Detection", "Use Cases"]),
        ("Production Basics", ["Pipeline Building", "Model Validation", "Monitoring Fundamentals", "ML Project"]),
    ],
    "dl": [
        ("Neural Network Basics", ["Perceptron and Neurons", "Backpropagation", "Activation Functions", "Optimization"]),
        ("PyTorch Workflow", ["Tensors and Autograd", "Building Models", "Training Loops", "Debugging Models"]),
        ("Deep Architectures", ["CNN Fundamentals", "RNN and Sequence Models", "Transfer Learning", "Regularization"]),
        ("Deployment Readiness", ["Model Saving", "Inference Pipelines", "Performance Tuning", "DL Capstone"]),
    ],
    "web": [
        ("Web Foundations", ["HTTP and Web Architecture", "Routing and Views", "Template Rendering", "Form Handling"]),
        ("Data & Auth", ["Database Models", "CRUD Operations", "Authentication", "Authorization"]),
        ("API Layer", ["REST Design", "Validation", "Error Handling", "API Security"]),
        ("Deployment", ["Environment Management", "Testing Basics", "Production Deployment", "Monitoring"]),
    ],
    "frontend": [
        ("Frontend Foundations", ["Modern JS Syntax", "DOM and Events", "Asynchronous JS", "Module Systems"]),
        ("Component Architecture", ["Component Design", "State and Props", "Hooks and Effects", "Reusable Patterns"]),
        ("UX and Performance", ["Responsive Layouts", "Accessibility Basics", "Performance Optimization", "Error Boundaries"]),
        ("Real Project", ["API Integration", "State Management", "Build and Deploy", "Portfolio Project"]),
    ],
    "backend": [
        ("Backend Foundations", ["Service Architecture", "Routing", "Middleware", "Error Handling"]),
        ("Data Layer", ["Schema Design", "Database Access", "Query Optimization", "Caching"]),
        ("Security", ["Auth and Sessions", "Input Validation", "Rate Limiting", "Logging and Audit"]),
        ("Production", ["Testing APIs", "CI/CD Basics", "Deployment", "Service Monitoring"]),
    ],
    "devops": [
        ("DevOps Basics", ["CLI and Shell", "Linux Filesystem", "Permissions", "Automation Scripts"]),
        ("Containers", ["Docker Images", "Docker Compose", "Container Networking", "Container Security"]),
        ("Orchestration", ["Kubernetes Objects", "Deployments", "Services and Ingress", "Config and Secrets"]),
        ("Delivery", ["CI/CD Pipelines", "Release Strategies", "Observability", "Incident Handling"]),
    ],
    "cloud": [
        ("Cloud Basics", ["Cloud Service Models", "IAM Principles", "Networking Concepts", "Cost Awareness"]),
        ("Core Services", ["Compute", "Storage", "Managed Databases", "Serverless Intro"]),
        ("Security & Reliability", ["Monitoring", "Backups", "High Availability", "Security Best Practices"]),
        ("Architecture", ["Reference Architectures", "Scaling Patterns", "Disaster Recovery", "Cloud Project"]),
    ],
    "security": [
        ("Security Fundamentals", ["Threat Modeling", "CIA Triad", "Attack Surface", "Security Controls"]),
        ("Network Security", ["Firewalls and Segmentation", "Vulnerability Scanning", "Traffic Analysis", "Hardening"]),
        ("Application Security", ["OWASP Basics", "Secure Coding", "Auth Weaknesses", "Testing and Reporting"]),
        ("Ethical Practice", ["Legal Scope", "Engagement Planning", "Pen Test Workflow", "Final Assessment"]),
    ],
    "mobile": [
        ("Mobile Basics", ["Project Setup", "UI Components", "Navigation", "State Management"]),
        ("Data and APIs", ["Networking", "Local Storage", "Authentication", "Error States"]),
        ("Platform Features", ["Device APIs", "Permissions", "Performance Tuning", "Accessibility"]),
        ("Publish Workflow", ["Testing", "Build Variants", "Store Readiness", "Mobile Capstone"]),
    ],
    "design": [
        ("Design Foundations", ["Design Principles", "Color and Typography", "Visual Hierarchy", "Layout Systems"]),
        ("UX Research", ["User Interviews", "Personas", "Journey Mapping", "Problem Framing"]),
        ("Prototyping", ["Wireframing", "Interactive Prototypes", "Design Systems", "Handoff Basics"]),
        ("Usability", ["Testing Methods", "Heuristic Reviews", "Iteration Workflow", "Portfolio Case Study"]),
    ],
    "se": [
        ("Engineering Foundations", ["SDLC", "Requirements", "Architecture Basics", "Code Quality"]),
        ("Testing and Reliability", ["Unit Testing", "Integration Testing", "Debugging", "Resilience Patterns"]),
        ("Collaboration", ["Version Control Workflow", "Code Reviews", "Documentation", "Agile Practices"]),
        ("Delivery", ["Release Planning", "Monitoring", "Maintenance", "Engineering Capstone"]),
    ],
    "dsa": [
        ("Core Structures", ["Arrays and Strings", "Linked Lists", "Stacks and Queues", "Hash Maps"]),
        ("Tree and Graph", ["Trees", "Binary Search Trees", "Graphs", "Traversal Techniques"]),
        ("Algorithms", ["Sorting", "Searching", "Recursion", "Dynamic Programming"]),
        ("Interview Practice", ["Problem Patterns", "Complexity Analysis", "Mock Problems", "Revision Sprint"]),
    ],
    "ai": [
        ("AI Overview", ["AI Landscape", "Problem Formulation", "Data and Features", "Model Evaluation"]),
        ("Classical AI", ["Search Methods", "Knowledge Representation", "Rule Systems", "Planning Basics"]),
        ("ML for AI", ["Supervised Models", "Unsupervised Models", "Experiment Tracking", "Failure Analysis"]),
        ("Responsible AI", ["Bias and Fairness", "Explainability", "Privacy", "AI Project"]),
    ],
    "nlp": [
        ("Language Foundations", ["Text Processing", "Tokenization", "Stemming and Lemmatization", "Vectorization"]),
        ("Sequence Models", ["Embeddings", "RNN/LSTM Basics", "Attention", "Transformer Overview"]),
        ("Applied NLP", ["Classification", "Named Entity Recognition", "Summarization", "Question Answering"]),
        ("Evaluation", ["Metrics", "Error Analysis", "Model Tuning", "NLP Capstone"]),
    ],
    "cv": [
        ("Vision Foundations", ["Image Basics", "Color Spaces", "Filtering", "Feature Extraction"]),
        ("Deep Vision", ["CNN Layers", "Transfer Learning", "Data Augmentation", "Object Detection Intro"]),
        ("Vision Tasks", ["Classification", "Segmentation", "Tracking Basics", "OCR Overview"]),
        ("Deployment", ["Inference Pipelines", "Optimization", "Edge Considerations", "CV Project"]),
    ],
}


def choose_image(title, domain_name):
    title_low = title.lower()
    for key, img in IMAGE_BY_KEYWORD.items():
        if key in title_low:
            return img

    domain_defaults = {
        "web development": "react_js.png",
        "data science": "data_analytics_powerbi.png",
        "artificial intelligence": "deep_learning.jpeg",
        "cloud computing": "aws.png",
        "cyber security": "network_security.jpg",
        "mobile app development": "flutter.png",
        "software engineering": "nextjs.jpg",
    }
    return domain_defaults.get(domain_name.lower(), "default_course.png")


def normalized(text):
    return (text or "").strip().lower()


def is_noise_course(title):
    t = normalized(title)
    return any(pattern in t for pattern in NOISE_PATTERNS)


def ensure_domains(catalog):
    domain_map = {normalized(d.name): d for d in Domain.query.all()}
    created = 0
    for item in catalog:
        domain_name = item["domain"].strip()
        key = normalized(domain_name)
        if key not in domain_map:
            domain = Domain(name=domain_name, description=f"{domain_name} learning path")
            db.session.add(domain)
            db.session.flush()
            domain_map[key] = domain
            created += 1
    return domain_map, created


def ensure_course(item, domain_map):
    title = item["title"].strip()
    existing = Course.query.filter(func.lower(Course.title) == title.lower()).first()
    created = False
    if not existing:
        domain = domain_map[normalized(item["domain"])]
        existing = Course(
            title=title,
            description=item["description"],
            domain_id=domain.id,
            price=0.0,
            instructor=item["instructor"],
            image_url=choose_image(title, item["domain"]),
            demo_video_url="https://www.youtube.com/watch?v=rfscVS0vtbw",
            status="published",
        )
        db.session.add(existing)
        db.session.flush()
        created = True
    else:
        if existing.status != "published":
            existing.status = "published"
        if not (existing.description or "").strip():
            existing.description = item["description"]
        if not (existing.instructor or "").strip():
            existing.instructor = item["instructor"]
        if not (existing.image_url or "").strip():
            existing.image_url = choose_image(title, item["domain"])
    return existing, created


def ensure_modules_and_lessons(course, track):
    module_blueprint = MODULE_TEMPLATES.get(track, MODULE_TEMPLATES["se"])
    created_modules = 0
    created_lessons = 0

    existing_modules = {
        normalized(m.title): m
        for m in CourseModule.query.filter_by(course_id=course.id).all()
    }

    for idx, (module_title, lessons) in enumerate(module_blueprint, start=1):
        key = normalized(module_title)
        module = existing_modules.get(key)
        if not module:
            module = CourseModule(course_id=course.id, title=module_title, order_index=idx)
            db.session.add(module)
            db.session.flush()
            existing_modules[key] = module
            created_modules += 1
        elif not module.order_index:
            module.order_index = idx

        existing_lesson_titles = {
            normalized(v.title)
            for v in Video.query.filter_by(course_id=course.id, module_id=module.id).all()
        }

        for lesson_title in lessons:
            lkey = normalized(lesson_title)
            if lkey in existing_lesson_titles:
                continue
            order_number = (
                db.session.query(func.max(Video.order_number))
                .filter(Video.course_id == course.id)
                .scalar()
            )
            next_order = int(order_number or 0) + 1
            url = VIDEO_URLS[(next_order - 1) % len(VIDEO_URLS)]
            db.session.add(
                Video(
                    course_id=course.id,
                    module_id=module.id,
                    title=lesson_title,
                    video_url=url,
                    description=f"{lesson_title} in {course.title}",
                    duration="10:00",
                    order_number=next_order,
                )
            )
            created_lessons += 1

    return created_modules, created_lessons


def ensure_syllabus(course):
    if Syllabus.query.filter_by(course_id=course.id).count() > 0:
        return 0

    lessons = (
        Video.query.filter_by(course_id=course.id)
        .order_by(Video.order_number.asc(), Video.id.asc())
        .limit(8)
        .all()
    )
    created = 0
    for idx, lesson in enumerate(lessons, start=1):
        db.session.add(
            Syllabus(
                course_id=course.id,
                topic_title=lesson.title,
                topic_description=f"Core concept: {lesson.title}",
                order_number=idx,
            )
        )
        created += 1
    return created


def main():
    with app.app_context():
        before_courses = Course.query.count()
        before_modules = CourseModule.query.count()
        before_lessons = Video.query.count()

        meaningful_existing = [
            c for c in Course.query.all()
            if not is_noise_course(c.title)
        ]

        domain_map, domains_created = ensure_domains(CATALOG)

        created_courses = 0
        published_updated = 0
        created_modules = 0
        created_lessons = 0
        created_syllabus = 0

        for item in CATALOG:
            course, was_created = ensure_course(item, domain_map)
            if was_created:
                created_courses += 1
            if course.status == "published":
                published_updated += 1

            m_count, l_count = ensure_modules_and_lessons(course, item["track"])
            created_modules += m_count
            created_lessons += l_count
            created_syllabus += ensure_syllabus(course)

        db.session.commit()

        after_courses = Course.query.count()
        after_modules = CourseModule.query.count()
        after_lessons = Video.query.count()
        published_total = Course.query.filter_by(status="published").count()

        print("Catalog restoration complete")
        print(f"domains_created={domains_created}")
        print(f"courses_created={created_courses}")
        print(f"published_courses_total={published_total}")
        print(f"modules_created={created_modules}")
        print(f"lessons_created={created_lessons}")
        print(f"syllabus_created={created_syllabus}")
        print(f"before_courses={before_courses}, after_courses={after_courses}")
        print(f"before_modules={before_modules}, after_modules={after_modules}")
        print(f"before_lessons={before_lessons}, after_lessons={after_lessons}")
        print(f"meaningful_existing_before={len(meaningful_existing)}")


if __name__ == "__main__":
    main()
