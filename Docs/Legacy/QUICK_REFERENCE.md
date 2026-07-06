# 🎓 Education Portal - Quick Reference

## 🚀 Start Application
```bash
cd d:\Edu Portal
python app.py
```
**Visit**: http://localhost:5000

---

## 📱 4 Main Pages

### 1. Homepage (/)
- Featured courses display
- Portal statistics
- Call-to-action buttons

### 2. Courses (/courses)
- ➕ Add new course
- ➕ Add video to course
- 🗑️ Delete course
- 🗑️ Delete video
- View course details

### 3. About (/about)
- Portal mission
- Features list
- Why choose us

### 4. Contact (/contact)
- Contact form
- Contact information
- Message history

---

## ✅ Validation Rules

### Email
- Must contain @ symbol
- Must have domain.extension
- Examples: user@example.com ✓, invalid-email ✗

### URLs
- Must start with http:// or https://
- Examples: https://site.com ✓, just-text ✗

### Form Fields
- Name: 2-100 chars
- Email: Valid format
- Subject: 3-200 chars
- Message: 5-1000 chars
- Course Title: 3-100 chars
- Video Title: 3-100 chars

---

## 🎥 Video Support

### YouTube
URLs that work:
- https://www.youtube.com/watch?v=VIDEO_ID
- https://youtu.be/VIDEO_ID
- https://www.youtube.com/embed/VIDEO_ID

### Other Platforms
- Vimeo links work as direct links
- Any platform URL works (opens in new tab)

---

## ⚠️ Error Messages

| Message | Meaning | Solution |
|---------|---------|----------|
| "Please fill in all fields!" | Missing data | Complete all required fields |
| "Please enter a valid email address!" | Bad email format | Use user@domain.com format |
| "Please enter a valid video URL..." | Bad URL format | Use http:// or https:// |
| "must be between X and Y characters" | Wrong length | Check character count |
| "Error saving..." | Database problem | Try again, refresh page |

---

## 🗑️ Delete Operations

### Delete a Video
1. Go to Courses page
2. Find course → "Add Video" section
3. Click Delete on video
4. Confirm deletion

### Delete a Course
1. Go to Courses page
2. Click "Delete" button on course card
3. Confirm deletion
4. All videos in course deleted too

---

## 📊 File Types

| File | Purpose |
|------|---------|
| app.py | Flask application |
| requirements.txt | Python packages |
| style.css | Styling |
| *.html | Web pages |
| portal.db | Database (auto-created) |

---

## 🔧 Common Tasks

### Add a Course
1. Go to Courses page
2. Fill "Add New Course" form
3. Click "Add Course"

### Add Video to Course
1. On Courses page, find course
2. Fill "Add Video to This Course"
3. Paste video URL
4. Click "Add Video"

### View Course
1. On homepage or courses page
2. Click "View Course"
3. See all videos in course

### Contact Portal
1. Go to Contact page
2. Fill contact form
3. Click "Send Message"
4. Message appears in Recent Messages

---

## 🆘 Troubleshooting

### App Won't Start
```bash
pip install -r requirements.txt
python app.py
```

### Port 5000 in Use
```bash
python app.py --port=5001
```

### Database Error
```bash
# Delete database and restart
rm portal.db
python app.py
```

### YouTube Video Not Embedding
- Check URL format
- Use one of: watch?v=, youtu.be/, embed/
- Direct link still works!

---

## 📞 Error Pages

| Status | Page | Meaning |
|--------|------|---------|
| 404 | Not Found | Page doesn't exist |
| 500 | Server Error | Backend problem |
| 400 | Bad Request | Invalid data |

All error pages have "Go Back Home" link.

---

## ✨ Features Tested & Working

✅ Create courses
✅ Add videos
✅ Delete videos
✅ Delete courses
✅ View courses
✅ Contact form
✅ Email validation
✅ URL validation
✅ YouTube embedding
✅ Error handling
✅ Error pages
✅ Responsive design

---

## 🎯 Pro Tips

1. **YouTube URLs**: Use short form `youtu.be/ID` for easy copying
2. **Descriptions**: Optional but helpful for users
3. **Course Names**: Be specific (not just "Course 1")
4. **Videos**: Order matters - add in sequence
5. **Contact**: Check Recent Messages section to see inquiries

---

## 📈 Statistics

- **Total Courses**: Shows on homepage
- **Total Videos**: Shows on homepage
- **Messages**: All contact messages saved with timestamp

---

**Version**: 2.0 (Full Error Handling)
**Last Updated**: March 7, 2026
**Status**: ✅ Verified against the current implementation baseline

<!-- BEGIN LATEST STATUS -->
## Latest Implementation Status (2026-03-08)

This section reflects the current stable implementation after Phase 5 governance and operations work.

### Current Phase State

1. Phase 1 data UX and performance baseline is active (search, filters, pagination, richer admin tables, query optimization).
2. Phase 2 workflow and authoring improvements are active (course builder, lifecycle states, drag-drop ordering, inline updates, publish guards).
3. Phase 3 analytics was intentionally removed (charts and chatbot analytics console are no longer part of admin dashboard).
4. Phase 4 security hardening is active (RBAC, CSRF enforcement, login/session protections, safer destructive actions).
5. Phase 5 governance and operations is active (bulk course actions, exports, quality alerts, activity tracking, immutable audit logs, role-aware admin navigation).

### Operational Features Now Available

- Role-aware admin sidebar navigation.
- Bulk course actions: review, publish (with publish guards), archive.
- CSV exports for courses, enrollments, and referrals.
- Content quality alerts on dashboard:
  - courses missing syllabus
  - courses missing videos
  - stale draft/review courses older than 30 days
- Admin activity page and full audit log page.
- System alerts page using read-only operational/security indicators.
- Destructive action approval workflow with explicit confirmation phrase.

### Security Baseline

- RBAC route-level permissions for `super_admin`, `content_admin`, and `support_analyst`.
- CSRF validation for admin POST requests.
- Admin login rate limiting and lockout handling.
- Admin session timeout enforcement.
- Immutable audit log records for governance and traceability.

### Removed Items (Intentional)

- Dashboard time-series analytics charts.
- Chatbot analytics console and `/admin/chatbot-analytics` route.

### Verification Snapshot

- Admin core pages load successfully (dashboard, courses, students, enrollments, referrals).
- New operational pages load successfully (`/admin/activity`, `/admin/audit-logs`, `/admin/system-alerts`).
- CSV export endpoints respond successfully.
- Public student flows remain functional (browse courses, course details, enrollment, course video access).

<!-- END LATEST STATUS -->




## Latest Updates (2026-03-08)

- Layout: Base shell moved to full-width wrappers (container-fluid px-4) and global responsive spacing was updated.
- Navigation: Role-aware Dashboard link added in navbar (student -> /student/dashboard, dmin -> /admin/dashboard), hidden for logged-out users.
- Logout UX: Added Logout links in navbar, student dashboard, and admin dashboard using existing /auth/logout route.
- Course visibility: Public/student course listings now show only published courses and exclude temporary noise titles (Phase2/Stability/Test-course patterns).
- Catalog restoration: Added safe script 
estore_catalog.py (non-destructive) to publish/add missing professional courses and attach modules/lessons/syllabus without duplicate titles.
- Catalog run result: courses created 26, modules created 108, lessons created 432, published courses available 27.
- Compatibility note: Existing LMS core flows (enrollment, modules, lessons, quizzes, assignments, dashboards) were preserved.

