from backend.app import app
from backend.models import db, Course

with app.app_context():
    courses = Course.query.all()

    for course in courses:
        if course.image_url and "placeholder" in course.image_url:
            print("Cleaning placeholder image for:", course.title)
            course.image_url = None

    db.session.commit()

print("Database cleaned successfully.")
