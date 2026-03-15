# Image Management Guide - Edu Portal

## Directory Structure

```
static/
├── images/
│   ├── courses/          👈 Store course images here
│   └── domains/          👈 Store domain images here
├── css/
├── js/
└── style.css
```

## Where to Paste Images

### 1. **Course Images**
- **Location**: `static/images/courses/`
- **File Types**: JPG, PNG, GIF, WebP
- **Recommended Size**: 300x200px or 600x400px (for better quality)
- **Naming Convention**: Use course name or ID
  - Example: `python_101.jpg`, `course_2.png`, `web_dev_basics.jpg`

### 2. **Domain Images**
- **Location**: `static/images/domains/`
- **File Types**: JPG, PNG, GIF, WebP
- **Recommended Size**: 300x300px or 400x400px (for logos/category images)
- **Naming Convention**: Use domain name or ID
  - Example: `programming.jpg`, `web_development.png`, `mobile_apps.jpg`

## How to Use Images in Admin Panel

### **Option 1: Upload via File (Recommended)**
1. Go to Admin Dashboard → Manage Courses
2. Click "Add New Course"
3. Fill in all course details
4. Use the **"Upload Course Image"** field to select image from your computer
5. System automatically saves to `static/images/courses/`
6. Click "Add Course"

### **Option 2: Paste Image Manually**
1. Copy/paste your image files directly to:
   - **For Courses**: `D:\Edu Portal\static\images\courses\`
   - **For Domains**: `D:\Edu Portal\static\images\domains\`
2. In Admin Panel, use the URL field:
   - Example: `/static/images/courses/python_101.jpg`
3. Update the course and save

### **Option 3: Use External URLs**
If you have images hosted online:
1. In Admin Panel, paste the full URL:
   - Example: `https://example.com/images/course.jpg`
2. Save and the image loads from external source

## Image Integration in Frontend

### **Homepage - Course Cards**
```html
<img src="{{ course.image_url }}" alt="{{ course.title }}">
```
- Displays course image on homepage cards
- Falls back to placeholder if image not found

### **Course Details Page**
```html
<img src="{{ course.image_url }}" alt="{{ course.title }}">
```
- Shows larger course image at top of course details
- Used as hero image

### **Domain Listing** (Coming Soon)
```html
<img src="{{ domain.image_url }}" alt="{{ domain.name }}">
```
- Displays domain/category image

## Database Fields

### **Course Model**
```python
course.image_url = "/static/images/courses/course_name.jpg"
```

### **Domain Model**
```python
domain.image_url = "/static/images/domains/domain_name.jpg"
```

## Step-by-Step Image Upload Instructions

### **Method A: Direct File Paste (Easiest)**
1. Open File Explorer
2. Navigate to: `D:\Edu Portal\static\images\courses\`
3. Right-click → Paste your image files here
4. In Admin Panel, use path: `/static/images/courses/your_image.jpg`

### **Method B: Copy from Downloads**
```powershell
# Copy course image from Downloads
Copy-Item "C:\Users\YourName\Downloads\python.jpg" "D:\Edu Portal\static\images\courses\"

# Copy domain image from Downloads
Copy-Item "C:\Users\YourName\Downloads\programming_logo.jpg" "D:\Edu Portal\static\images\domains\"
```

### **Method C: Admin Panel File Upload** (When Available)
1. Navigate to Admin Dashboard
2. Click "Add New Course"
3. Click "Choose File" button next to "Upload Course Image"
4. Select image from your computer
5. System handles upload automatically

## Common Image Paths Used

```
/static/images/courses/python_basics.jpg
/static/images/courses/web_development.png
/static/images/courses/data_science.jpg
/static/images/courses/mobile_apps.png

/static/images/domains/programming.jpg
/static/images/domains/web_design.jpg
/static/images/domains/data_science.jpg
```

## Troubleshooting

### **Image Not Showing?**
- ❌ Check file path is correct
- ❌ Verify file exists in correct folder
- ❌ Check file permissions (readable by Flask)
- ✅ Use absolute path: `/static/images/courses/image.jpg`

### **Image Upload Failed?**
- ✅ Folders exist: `static/images/courses/` and `static/images/domains/`
- ✅ File size < 5MB
- ✅ File format is JPG, PNG, GIF, or WebP
- ✅ Filename has no special characters

## Image Display Across App

| Page | Image Field | Location |
|------|-------------|----------|
| Homepage | Course Card Image | `templates/public/index.html` |
| Course Listing | Course Thumbnail | `templates/student/courses.html` |
| Course Details | Course Hero Image | `templates/student/course_details.html` |
| Admin Management | Course Thumbnail | `templates/admin/manage_courses.html` |
| Admin Edit | Current Image Preview | `templates/admin/edit_course.html` |

## Next Steps

1. **Create Image Folders** ✅ (Already Done)
2. **Paste Your Images** into:
   - `D:\Edu Portal\static\images\courses\`
   - `D:\Edu Portal\static\images\domains\`
3. **Update Admin Forms** to add image path in database
4. **Update Templates** to display images (already configured)
5. **Test on Homepage** - images should appear on course cards

## Best Practices

✅ **Do:**
- Use consistent naming convention
- Optimize images before uploading (use TinyPNG or similar)
- Use descriptive filenames: `python_101.jpg` not `pic123.jpg`
- Keep images under 500KB for fast loading
- Use relative paths in database: `/static/images/courses/...`

❌ **Don't:**
- Use absolute path on Windows: `D:\Edu Portal\static\...` (won't work on other systems)
- Mix local files and external URLs inconsistently
- Use special characters in filenames
- Upload images > 5MB (slow loading)

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

