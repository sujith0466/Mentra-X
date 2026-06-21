#!/usr/bin/env python3
"""
Database Seeding Script
Populates the Education Portal database with sample domains and courses.
"""

from backend.app import app, db
from backend.models import Domain, Course, Syllabus, User

def seed_database():
    """Seed the database with sample data"""
    
    with app.app_context():
        print("🌱 Starting database seeding...")
        
        # Drop all existing tables to ensure clean state
        db.drop_all()
        print("✓ Dropped existing tables")
        
        # Create tables
        db.create_all()
        print("✓ Database tables created")
        
        # Define domains
        domains_data = [
            {
                'name': 'Web Development',
                'description': 'Learn to build modern web applications using HTML, CSS, JavaScript, and popular frameworks'
            },
            {
                'name': 'Data Science',
                'description': 'Master data analysis, machine learning, and statistical techniques'
            },
            {
                'name': 'Artificial Intelligence',
                'description': 'Explore AI, deep learning, neural networks, and advanced algorithms'
            },
            {
                'name': 'Cyber Security',
                'description': 'Learn security analysis, penetration testing, and information protection'
            },
            {
                'name': 'Cloud Computing',
                'description': 'Deploy and manage applications on AWS, Azure, and GCP'
            },
            {
                'name': 'Mobile App Development',
                'description': 'Build native and cross-platform mobile applications'
            }
        ]
        
        # Add domains
        domains = {}
        for domain_data in domains_data:
            domain = Domain.query.filter_by(name=domain_data['name']).first()
            if not domain:
                domain = Domain(**domain_data)
                db.session.add(domain)
                print(f"  Adding domain: {domain_data['name']}")
            domains[domain_data['name']] = domain
        
        db.session.commit()
        print("✓ Domains created")
        
        # Define courses
        courses_data = [
            # Web Development Courses
            {
                'title': 'React JS - Modern Web Development',
                'description': 'Learn React from basics to advanced. Build interactive user interfaces with hooks, context API, and state management.',
                'domain_name': 'Web Development',
                'instructor': 'John Developer',
                'price': 2999,
                'image_url': 'react_js.png',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': 'Python Flask - Full Stack Development',
                'description': 'Master backend development with Flask. Build scalable web applications with database integration and API design.',
                'domain_name': 'Web Development',
                'instructor': 'Sarah Backend',
                'price': 1999,
                'image_url': 'flask_fullstack.jpg',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': 'Next.js - Advanced React Framework',
                'description': 'Build full-stack React applications with Next.js. Server-side rendering, static generation, and API routes explained.',
                'domain_name': 'Web Development',
                'instructor': 'Alex Smith',
                'price': 2499,
                'image_url': 'nextjs.jpg',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': 'MERN Stack - Complete Web Development',
                'description': 'Full-stack JavaScript development. MongoDB, Express, React, Node.js - build complete web applications.',
                'domain_name': 'Web Development',
                'instructor': 'Mike Johnson',
                'price': 3499,
                'image_url': 'mern_stack.jpg',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            
            # Data Science Courses
            {
                'title': 'Python for Data Science',
                'description': 'Learn Python fundamentals for data analysis. Libraries like pandas, NumPy, matplotlib, and scikit-learn.',
                'domain_name': 'Data Science',
                'instructor': 'Dr. Emma Watson',
                'price': 1899,
                'image_url': 'python_datascience.jpg',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': 'Machine Learning Fundamentals',
                'description': 'Understand supervised learning, unsupervised learning, and evaluation metrics. Real-world ML projects included.',
                'domain_name': 'Data Science',
                'instructor': 'Prof. Andrew Ng',
                'price': 3199,
                'image_url': 'machine_learning.jpg',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': 'Data Analytics with Power BI',
                'description': 'Master business intelligence. Create interactive dashboards, reports, and data visualizations with Power BI.',
                'domain_name': 'Data Science',
                'instructor': 'Lisa Analytics',
                'price': 2299,
                'image_url': 'data_analytics_powerbi.png',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            
            # AI Courses
            {
                'title': 'Deep Learning - Neural Networks',
                'description': 'Build deep neural networks with TensorFlow and PyTorch. CNNs, RNNs, and transformers explained.',
                'domain_name': 'Artificial Intelligence',
                'instructor': 'Dr. Yann LeCun',
                'price': 4299,
                'image_url': 'deep_learning.jpeg',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': 'Natural Language Processing (NLP)',
                'description': 'Process and analyze text data. Transformers, BERT, GPT, and building NLP applications.',
                'domain_name': 'Artificial Intelligence',
                'instructor': 'Dr. Yoshua Bengio',
                'price': 3599,
                'image_url': 'nlp.jpg',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            
            # Cyber Security Courses
            {
                'title': 'Ethical Hacking & Penetration Testing',
                'description': 'Learn to identify vulnerabilities and test security. Tools like Metasploit, Burp Suite, and Nmap.',
                'domain_name': 'Cyber Security',
                'instructor': 'Kevin Mitnick',
                'price': 3999,
                'image_url': 'ethical_hacking.png',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': 'Network Security Fundamentals',
                'description': 'Secure network design and implementation. Firewalls, VPNs, intrusion detection, and more.',
                'domain_name': 'Cyber Security',
                'instructor': 'James Security',
                'price': 2799,
                'image_url': 'network_security.jpg',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            
            # Cloud Computing Courses
            {
                'title': 'AWS Cloud Computing Mastery',
                'description': 'Master Amazon Web Services. EC2, S3, Lambda, RDS, and building scalable cloud applications.',
                'domain_name': 'Cloud Computing',
                'instructor': 'Andy Jassy',
                'price': 3299,
                'image_url': 'aws.png',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': 'Kubernetes & Docker - Container Mastery',
                'description': 'Containerize applications with Docker. Orchestrate with Kubernetes. DevOps best practices.',
                'domain_name': 'Cloud Computing',
                'instructor': 'Kelsey Hightower',
                'price': 3599,
                'image_url': 'docker_kubernetes.png',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            
            # Mobile App Development
            {
                'title': 'React Native - Cross-Platform Mobile Apps',
                'description': 'Build iOS and Android apps with React Native. Single codebase for multiple platforms.',
                'domain_name': 'Mobile App Development',
                'instructor': 'Mark Brown',
                'price': 2999,
                'image_url': 'react_native.png',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
            {
                'title': 'Flutter Development - Beautiful Apps',
                'description': 'Create stunning mobile apps with Flutter. Widget-based UI, fast development, and great performance.',
                'domain_name': 'Mobile App Development',
                'instructor': 'Google Developers',
                'price': 2699,
                'image_url': 'flutter.png',
                'demo_video_url': 'https://www.youtube.com/embed/dQw4w9WgXcQ'
            },
        ]
        
        # Add courses
        for course_data in courses_data:
            domain_name = course_data.pop('domain_name')
            domain = domains[domain_name]
            
            # Check if course already exists
            existing_course = Course.query.filter_by(title=course_data['title']).first()
            if not existing_course:
                course = Course(domain_id=domain.id, **course_data)
                db.session.add(course)
                print(f"  Adding course: {course_data['title']} ({domain_name})")
        
        db.session.commit()
        print("✓ Courses created")
        
        # Add sample syllabuses for a few courses
        python_course = Course.query.filter_by(title='Python for Data Science').first()
        if python_course and len(python_course.syllabuses) == 0:
            syllabus_topics = [
                'Python Basics and Syntax',
                'NumPy - Numerical Computing',
                'Pandas - Data Manipulation',
                'Matplotlib & Seaborn - Data Visualization',
                'Statistical Analysis',
                'Data Cleaning and Preprocessing',
                'Feature Engineering',
                'Exploratory Data Analysis (EDA)',
            ]
            
            for i, topic in enumerate(syllabus_topics, 1):
                syllabus = Syllabus(
                    course_id=python_course.id,
                    topic_title=topic,
                    topic_description=f'Learn {topic} in depth with practical examples and exercises.',
                    order_number=i
                )
                db.session.add(syllabus)
            
            db.session.commit()
            print("✓ Sample syllabus added for Python course")
        
        print("\n✅ Database seeding completed successfully!")
        print(f"📊 Summary:")
        print(f"  - Domains: {Domain.query.count()}")
        print(f"  - Courses: {Course.query.count()}")
        print(f"  - Syllabus items: {Syllabus.query.count()}")

if __name__ == '__main__':
    seed_database()
