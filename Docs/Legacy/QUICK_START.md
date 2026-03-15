# Quick Start Guide - Education Portal

## ⚡ Start the Application in 30 Seconds

### Step 1: Navigate to Project Directory
```bash
cd "d:\Edu Portal"
```

### Step 2: Activate Virtual Environment (if using .venv)
```bash
.venv\Scripts\activate
```

### Step 3: Run the App
```bash
python app.py
```

### Step 4: Open in Browser
Visit: **http://127.0.0.1:5000**

---

## 🔐 Demo Accounts

### Admin Login
- **URL**: http://127.0.0.1:5000/auth/login
- **Email**: admin@eduportal.com
- **Password**: admin123
- **Features**: Manage courses, students, videos, domains

### Student Login
- **URL**: http://127.0.0.1:5000/auth/register
- Register new account
- Browse & enroll in courses
- Earn rewards through referral program

---

## 🎯 What to Try First

1. **Home Page**: http://127.0.0.1:5000/
   - View featured courses
   - See portal statistics
   - Ask the AI chatbot questions (bottom-right button)

2. **Browse Courses**: http://127.0.0.1:5000/courses
   - Filter by domain
   - View course details
   - Enroll in courses

3. **Test the Chatbot** (NEW! Phase 14 - Clickable Options)
   - Click any floating chat button on the site
   - Ask questions OR click the blue suggestion buttons
   - Suggested options appear after each response
   - Examples to try:
     - "What is Python?"
     - "What is Web Development?"
     - "Which course should I start with?"
     - "What is Data Science?"
   - Get instant hardcoded responses with smart suggestions (no API key needed!)

3. **Register as Student**: http://127.0.0.1:5000/auth/register
   - Create an account
   - Optionally enter a referral code

4. **Student Dashboard**: http://127.0.0.1:5000/student/dashboard (after login)
   - View your wallet
   - See referral info

5. **Admin Panel**: http://127.0.0.1:5000/admin/dashboard
   - Login with admin credentials
   - Manage courses and students

---

## 📋 Pre-loaded Setup

✓ Default admin user created  
✓ Database tables initialized  
✓ All routes configured  
✓ Templates ready  

---

## 🔧 Troubleshooting

**App won't start?**
```bash
# Install dependencies
pip install -r requirements.txt

# Try running again
python app.py
```

**Port 5000 in use?**
Edit `app.py` last line:
```python
app.run(debug=True, port=5001)  # Use different port
```

**Database error?**
```bash
# Delete and recreate database
del instance\portal.db
python app.py  # Restarts fresh
```

---

## 📂 Files You Can Customize

- `templates/base.html` - Navigation and layout
- `static/css/main.css` - Colors and styling  
- `app.py` - Secret key, database, configuration
- `models.py` - Database schema changes

---

## 🎓 Project Ready!

Your complete Education Portal with:
✅ Student authentication & dashboard  
✅ Course enrollment system  
✅ Video management  
✅ Referral rewards  
✅ Admin panel  
✅ Contact form  

Enjoy! 🚀

<!-- BEGIN LATEST STATUS -->
## Latest Implementation Status (2026-03-08)

This document reflects the latest implemented changes in the Education Portal.

### Completed Platform Updates

1. Homepage metrics are displayed in a horizontal 4-card layout.
2. Homepage course cards are improved (rounded corners, shadow, spacing, hover effect).
3. Spacing between "View All Courses" and "Why Choose EduPortal" was increased.
4. "Why Choose EduPortal" section layout/readability was improved.
5. Homepage cards show only course image and course name.
6. Admin dashboard statistic cards were visually enhanced.
7. "Welcome back" login flash now auto-disappears.
8. Course price is admin-managed and hidden from homepage cards.
9. Admin management supports add/view/edit/delete admins.
10. Syllabus management supports add/update/delete topics.
11. Video management supports add/update/delete videos.
12. Course image upload works in admin add/edit course forms.
13. Course image naming and mapping are aligned with `static/images/courses`.

### Course Image System (Current Behavior)

- Local images are stored in: `static/images/courses/`
- Local images are rendered via: `url_for('static', filename='images/courses/<filename>')`
- Images are shown on Homepage, Courses page, and Course detail page.
- Existing course records are synchronized at startup via `_sync_course_image_references()`.

### Final Operational Note

After image/path updates, restart Flask to apply synchronization:

```bash
python app.py
```

<!-- END LATEST STATUS -->



## Latest Updates (2026-03-08)

- Layout: Base shell moved to full-width wrappers (container-fluid px-4) and global responsive spacing was updated.
- Navigation: Role-aware Dashboard link added in navbar (student -> /student/dashboard, dmin -> /admin/dashboard), hidden for logged-out users.
- Logout UX: Added Logout links in navbar, student dashboard, and admin dashboard using existing /auth/logout route.
- Course visibility: Public/student course listings now show only published courses and exclude temporary noise titles (Phase2/Stability/Test-course patterns).
- Catalog restoration: Added safe script estore_catalog.py (non-destructive) to publish/add missing professional courses and attach modules/lessons/syllabus without duplicate titles.
- Catalog run result: courses created 26, modules created 108, lessons created 432, published courses available 27.
- Compatibility note: Existing LMS core flows (enrollment, modules, lessons, quizzes, assignments, dashboards) were preserved.

