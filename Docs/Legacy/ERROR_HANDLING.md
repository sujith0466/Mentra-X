# Education Portal - Error Handling & Validation Guide

## ✅ Comprehensive Error Handling Implemented

### 1. **Validation Functions**

#### `extract_youtube_id(url)`
Extracts YouTube video ID from multiple URL formats:
- `https://www.youtube.com/watch?v=VIDEO_ID`
- `https://youtu.be/VIDEO_ID`
- `https://www.youtube.com/embed/VIDEO_ID`
- `https://www.youtube.com/v/VIDEO_ID`

Returns `None` if URL is not a valid YouTube link.

#### `is_valid_url(url)`
Validates if a URL is properly formatted:
- Checks for valid scheme (http/https)
- Checks for valid network location
- Returns `True`/`False`

#### `is_valid_email(email)`
Validates email format using regex:
- Checks standard email format: `user@domain.com`
- Supports subdomains and multi-level TLDs
- Returns `True`/`False`

### 2. **Form Input Validation**

All forms validate inputs before database operations:

#### Contact Form Validation
- **Name**: 2-100 characters
- **Email**: Valid email format (validated by `is_valid_email()`)
- **Subject**: 3-200 characters
- **Message**: 5-1000 characters

#### Course Form Validation
- **Title**: 3-100 characters
- **Description**: Max 500 characters

#### Video Form Validation
- **Title**: 3-100 characters
- **URL**: Valid URL format (validated by `is_valid_url()`)
- **Description**: Max 500 characters

### 3. **Database Error Handling**

All database operations are wrapped in try-except blocks:

```python
try:
    # Database operation
    db.session.add(object)
    db.session.commit()
    flash('Success message', 'success')
except Exception as db_error:
    db.session.rollback()  # Rollback on error
    print(f"Database error: {db_error}")
    flash('Error saving. Please try again.', 'danger')
```

### 4. **Route Error Handlers**

#### Global Error Handlers
- **404 Not Found** - Custom error page displayed
- **500 Internal Server Error** - Custom error page with rollback
- **400 Bad Request** - Custom error page

All error handlers:
- Display user-friendly error messages
- Log detailed error information to console
- Rollback database transactions on errors
- Redirect users to safe pages

### 5. **Route-Level Error Handling**

All routes have try-except blocks for:
- Template rendering errors
- Database query errors
- Data processing errors

Each error:
- Logs detailed information to console
- Shows user-friendly flash message
- Gracefully handles exceptions without crashing

### 6. **Flash Messages**

Alert system with categories:
- **success** - Green background (✓ Operation completed)
- **danger** - Red background (✗ Error occurred)
- **info** - Blue background (ℹ Information)

Examples:
```
✓ Course added successfully!
✗ Please enter a valid email address!
✗ Error saving message. Please try again.
```

### 7. **Input Sanitization**

All user inputs are:
1. **Stripped** of leading/trailing whitespace
2. **Validated** against specific criteria
3. **Checked** for required fields
4. **Escaped** automatically by Jinja2 templates

### 8. **Video URL Handling**

Video URLs support:
- **YouTube** - Automatic extraction and player embedding
- **Vimeo** - Direct link opening
- **Other platforms** - Direct link opening with fallback display

If YouTube extraction fails:
- Shows placeholder instead of broken embed
- Provides direct URL link for user

### 9. **Database Integrity**

- Foreign key constraints enforce data relationships
- Cascade delete removes associated videos when course is deleted
- Automatic timestamp tracking for all records
- Safe NULL handling for optional fields

## 📋 Error Scenarios Handled

| Scenario | Handling |
|----------|----------|
| Invalid email format | Validation error, form resubmitted |
| Database connection lost | Error message, automatic rollback |
| Missing required fields | Validation error with clear message |
| Invalid video URL | URL format validation, error message |
| Non-existent course access | 404 error page displayed |
| Expired session | User redirected to login (future feature) |
| Invalid YouTube URL | Fallback placeholder shown |
| Server crash | 500 error page, transaction rollback |
| SQL injection attempt | Prevented by Flask-SQLAlchemy ORM |

## 🔒 Security Features

1. **SQL Injection Prevention** - Using ORM parameterized queries
2. **XSS Prevention** - Jinja2 auto-escaping enabled
3. **CSRF Protection** - Recommended for production (add Flask-WTF)
4. **Email Validation** - Prevents malformed email addresses
5. **URL Validation** - Ensures only valid URLs stored
6. **Input Sanitization** - All inputs stripped and validated

## 🚀 Running the Application

```bash
# Install dependencies
pip install -r requirements.txt

# Run development server
python app.py

# Run with tests
python test_validations.py
```

## 📝 Console Error Logging

All errors are logged to console for debugging:
```
Error loading index: [error details]
Database error: [specific error]
Invalid YouTube URL in video player: [fallback used]
```

## 🎯 Best Practices Implemented

✓ Comprehensive input validation
✓ Database transaction management
✓ Graceful error handling
✓ User-friendly error messages
✓ Console logging for debugging
✓ Automatic database rollback on errors
✓ Safe template rendering
✓ Proper HTTP status codes
✓ Custom error pages
✓ Video player fallback display

## 🔧 Future Enhancements

- Add Flask-WTF for CSRF protection
- Implement user authentication
- Add email verification
- Add file upload with validation
- Implement rate limiting
- Add request logging middleware
- Add performance monitoring

---

**Last Updated**: March 7, 2026
**Version**: 2.0 (Error-friendly Release)

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

