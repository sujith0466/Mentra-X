# Education Portal - Tutedude Inspired Platform

## Implementation Complete ✓

Your Education Portal has been successfully upgraded to a comprehensive learning platform with student authentication, course management, enrollment system, and a referral program - similar to platforms like Tutedude.

---

## 🎯 Project Overview

This is a full-featured educational platform built with Flask that includes:
- **Student Management**: Registration, login, enrollment, and progress tracking
- **Course Management**: Organized by domains with videos and syllabus
- **Admin Panel**: Complete course and user management
- **Referral System**: Students earn rewards by inviting friends
- **Responsive Design**: Works on desktop, tablet, and mobile devices

---

## 📁 Project Structure

```
Edu Portal/
├── app.py                          # Main Flask application
├── models.py                       # SQLAlchemy database models
├── auth_routes.py                  # Authentication (login/register)
├── student_routes.py               # Student features (dashboard, courses, referral)
├── admin_routes.py                 # Admin features (manage courses, students)
├── public_routes.py                # Public pages (home, courses, contact)
│
├── requirements.txt                # Python dependencies
│
├── templates/
│   ├── base.html                   # Base template with navigation
│   │
│   ├── auth/
│   │   ├── login.html              # Student/Admin login page
│   │   └── register.html           # Student registration page
│   │
│   ├── public/
│   │   ├── index.html              # Homepage with featured courses
│   │   ├── courses.html            # Browse courses (domain based)
│   │   ├── course_detail.html      # Course details, syllabus, videos
│   │   ├── about.html              # About us page
│   │   └── contact.html            # Contact form and messages
│   │
│   ├── student/
│   │   ├── dashboard.html          # Student dashboard
│   │   ├── my_courses.html         # Enrolled courses with progress
│   │   ├── course_videos.html      # Video player and syllabus
│   │   └── referral.html           # Referral program and earnings
│   │
│   ├── admin/
│   │   ├── dashboard.html          # Admin dashboard with statistics
│   │   ├── manage_courses.html     # View/add/edit courses
│   │   ├── manage_domains.html     # Manage learning domains
│   │   ├── manage_videos.html      # Upload videos to courses
│   │   ├── manage_students.html    # View all students
│   │   ├── manage_syllabus.html    # Add course syllabus topics
│   │   ├── view_enrollments.html   # View all enrollments
│   │   └── view_referrals.html     # View referral transactions
│   │
│   └── errors/
│       ├── 404.html                # Page not found error
│       ├── 500.html                # Server error page
│       └── 400.html                # Bad request error page
│
├── static/
│   ├── style.css                   # Original styles
│   ├── css/
│   │   └── main.css                # New comprehensive styles
│   └── js/
│       └── main.js                 # Frontend functionality
│
├── instance/
│   └── portal.db                   # SQLite database (auto-created)
│
└── Documentation/
    ├── README.md                   # Project readme
    ├── SETUP_GUIDE.md             # Setup instructions
    ├── DATABASE.md                 # Database schema
    └── API_ROUTES.md              # List of all routes
```

---

## 🗄️ Database Schema

### Users Table
- id, name, email, password (hashed)
- role (student/admin), referral_code, referred_by
- wallet_balance (for referral rewards)
- created_at

### Domains Table
- id, name, description
- Related: hasMany Courses

### Courses Table
- id, title, description, domain_id
- price, instructor, image_url
- Created_at
- Related: hasMany Videos, Syllabuses, Enrollments

### Syllabuses Table
- id, course_id, topic_title, topic_description
- order_number, created_at

### Videos Table
- id, course_id, title, video_url, description
- duration, order_number, created_at

### Enrollments Table
- id, user_id, course_id
- enrolled_date, progress (0-100%), completed (boolean)

### ContactMessages Table
- id, name, email, subject, message
- created_at

### ReferralTransactions Table
- id, referrer_id, new_user_id, reward_amount
- status (pending/completed), date

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7+ (tested with Python 3.13)
- pip (Python package manager)

### Installation

1. **Install Dependencies**
   ```bash
   cd "d:\Edu Portal"
   pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   python app.py
   ```

3. **Access the Portal**
   Open your browser and go to: `http://127.0.0.1:5000`

---

## 👤 Default Admin Credentials

The application automatically creates a default admin user on first run:

- **Email**: `admin@eduportal.com`
- **Password**: `admin123`

**⚠️ IMPORTANT**: Change these credentials in production!

---

## 📋 Main Features

### 1. Public Pages (No Login Required)
- **Home**: Featured courses and portal statistics
- **Courses**: Browse all courses organized by domains
- **Course Details**: View course syllabus, videos, and enroll
- **About**: Information about the portal
- **Contact**: Contact form for inquiries

### 2. Student Features (After Login)
- **Dashboard**: Overview of courses, referrals, and wallet
- **My Courses**: View enrolled courses with progress tracking
- **Course Videos**: Watch course videos (YouTube or direct links)
- **Progress Tracking**: Update course completion percentage
- **Referral Program**: 
  - Get unique referral code
  - Share referral link via WhatsApp, Twitter, Facebook
  - Earn ₹100 for each friend who registers
  - View referral history and earnings

### 3. Admin Features (Admin Login Required)
- **Dashboard**: Statistics and recent enrollments
- **Domain Management**: Create/manage learning domains
- **Course Management**: Add/edit/delete courses
- **Video Management**: Upload course videos
- **Syllabus Management**: Create course curriculum
- **Student Management**: View all registered students
- **Enrollment Tracking**: View all course enrollments
- **Referral Analytics**: Track referral transactions

### 4. Security Features
- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control (Student/Admin)
- Input validation and sanitization
- CSRF protection (Flask built-in)
- SQL injection prevention (SQLAlchemy ORM)

---

## 🔄 Referral System Logic

When a student registers with a referral code:

1. **Validation**: System checks if referral code is valid
2. **Reward Distribution**:
   - Referrer gets ₹100 in wallet balance
   - New user gets ₹100 in wallet balance
3. **Transaction Recording**: Referral transaction is logged
4. **Usage**: Wallet balance can be used for course discounts/certificates

Example Flow:
```
User A registers with code "USER_A123"
↓
User B registers using User A's referral code
↓
User A's wallet: ₹100
User B's wallet: ₹100
ReferralTransaction created with status=completed
```

---

## 📚 Learning Domains

The portal supports multiple learning domains:
- Data Science
- Web Development
- Artificial Intelligence
- Cloud Computing
- Cyber Security
- (Admin can add more)

Each domain can have multiple courses with videos and syllabus.

---

## 🔗 Key Routes

### Public Routes
- `GET /` - Home page
- `GET /courses` - Browse all courses
- `GET /course/<course_id>` - Course details
- `GET /about` - About page
- `GET /contact` - Contact page (GET for form, POST for submission)

### Authentication Routes
- `GET /auth/login` - Login form
- `POST /auth/login` - Process login
- `GET /auth/register?ref=<code>` - Registration form (optional referral code)
- `POST /auth/register` - Process registration
- `GET /auth/logout` - Logout

### Student Routes (Login Required)
- `GET /student/dashboard` - Student dashboard
- `GET /student/my-courses` - Enrolled courses
- `GET /student/course/<course_id>` - View course videos
- `POST /student/enroll/<course_id>` - Enroll in course
- `GET /student/referral` - Referral program page
- `POST /student/update-progress/<course_id>` - Update progress

### Admin Routes (Admin Login Required)
- `GET /admin/dashboard` - Admin dashboard
- `GET /admin/courses` - Manage courses
- `POST /admin/course/add` - Add course
- `GET /admin/course/<id>/edit` - Edit course
- `POST /admin/course/<id>/delete` - Delete course
- `GET /admin/course/<id>/videos` - Manage videos
- `POST /admin/video/add` - Add video
- `GET /admin/domains` - Manage domains
- `GET /admin/students` - View students
- `GET /admin/enrollments` - View enrollments
- `GET /admin/referrals` - View referrals

---

## 🛠️ Technology Stack

- **Frontend**: HTML5, CSS3, JavaScript
- **Backend**: Flask 2.3.3
- **Database**: SQLite3 with SQLAlchemy ORM
- **Authentication**: Flask Sessions + Password Hashing (Werkzeug)
- **Database Driver**: Flask-SQLAlchemy 3.1.1, SQLAlchemy 2.0.48 (Python 3.13 compatible)

---

## 📦 Dependencies

```
Flask==2.3.3           # Web framework
Flask-SQLAlchemy==3.1.1 # ORM wrapper
SQLAlchemy==2.0.48     # Object-relational mapping (Python 3.13 compatible)
Werkzeug==2.3.7        # WSGI utilities and password hashing
```

---

## ⚙️ Configuration

Edit `app.py` to customize:

```python
app.config['SECRET_KEY'] = 'your_secret_key_here'  # Change in production!
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///portal.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
```

---

## 🎨 Customization

### Change Color Scheme
Edit `static/css/main.css` and modify CSS variables:
```css
:root {
    --primary-color: #FF6B35;     /* Main color */
    --secondary-color: #F7931E;   /* Accent color */
    --success-color: #4CAF50;     /* Success color */
    /* ... more colors ... */
}
```

### Modify Navigation Menu
Edit `templates/base.html` to add/remove menu items

### Update Portal Name
Search for "EduPortal" in templates and replace with your brand name

---

## 🧪 Testing Accounts

### Admin Account (Created Automatically)
- Email: admin@eduportal.com
- Password: admin123

### Create Student Account
- Register at `/auth/register`
- Use referral code if available for bonus ₹100

---

## 📊 Database Location

SQLite database is stored at: `d:\Edu Portal\instance\portal.db`

To reset database:
1. Stop the application
2. Delete `instance/portal.db`
3. Restart the application (it will recreate)

---

## 🚨 Common Issues & Solutions

### Issue: "Module not found" error
**Solution**: Run `pip install -r requirements.txt`

### Issue: Port 5000 already in use
**Solution**: Change port in `app.py`:
```python
app.run(debug=True, host='127.0.0.1', port=5001)
```

### Issue: Database locked error
**Solution**: Close all running instances and restart Flask

### Issue: Videos not playing
**Solution**: Ensure video URLs are accessible and correct format

---

## 🚀 Deployment

For production deployment:

1. Change `debug=True` to `debug=False` in app.py
2. Use strong SECRET_KEY
3. Install production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn app:app
   ```
4. Use proper database (PostgreSQL recommended)
5. Set up SSL/HTTPS
6. Configure environment variables for sensitive data

---

## 📞 Support

For issues or questions:
- Email: info@eduportal.com
- Contact form: http://localhost:5000/contact

---

## 📄 License

This project is provided as-is for educational purposes.

---

## 🎉 Congratulations!

Your Tutedude-inspired Education Portal is ready to use!

**Next Steps**:
1. Customize the portal with your branding
2. Add domains and courses
3. Upload course videos
4. Create student accounts and test
5. Deploy to production

Enjoy teaching and learning! 📚✨

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

