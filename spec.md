# PROJECT: BICHU BIJU – PERSONAL ENGINEERING PORTFOLIO

Act as a senior full-stack developer, UI/UX designer, Python Django developer, and database architect.

Build a complete, modern, responsive, full-stack personal portfolio website for an engineering student specializing in Artificial Intelligence and Machine Learning.

The website must have two main parts:

1. Public Portfolio Website – Visitors can explore my profile, skills, projects, education, achievements, resume, and contact information.
2. Secure Admin Dashboard – Only the authorized administrator can log in and manage all website content without modifying source code.

The website must be fully functional, not just a static UI design.

---

# 1. TECHNOLOGY STACK

Frontend:
- HTML5
- CSS3
- JavaScript
- Bootstrap 5 or Tailwind CSS
- Responsive design
- Font Awesome or Lucide icons
- Smooth scrolling and animations

Backend:
- Python
- Django
- Django REST Framework
- Django Authentication
- REST API architecture

Database:
- Supabase PostgreSQL
- Django ORM
- Secure database connection using environment variables
- Database migrations

Storage:
- Supabase Storage for profile images, project images, certificates, and resume files.

Important:
Use Supabase primarily as the PostgreSQL database and file storage provider. Connect Django to Supabase PostgreSQL using its supported connection string and SSL configuration. Do not expose database credentials or service-role keys in frontend code.

---

# 2. WEBSITE DESIGN AND UI/UX

Design the website based on the provided reference image.

Design style:
- Minimalist white background.
- Black typography.
- Professional engineering portfolio appearance.
- Large profile image.
- Engineering-related illustrations.
- Clean navigation.
- Rounded image corners.
- Subtle shadows.
- Smooth hover effects.
- Modern typography.
- Plenty of white space.

Color palette:
- Primary background: #FFFFFF
- Primary text: #111111
- Secondary text: #666666
- Accent color: #263A59
- Button background: #263A59
- Light section background: #F7F8FA

Avoid excessive gradients, unnecessary animations, and overcrowded layouts.

The design should look like a professional portfolio created by a modern engineering student.

---

# 3. NAVIGATION BAR

Create a fixed or sticky navigation bar.

Top-left navigation:
- Home
- Resume
- Projects
- Skills
- Contact

Center:
- Bichu Biju's Portfolio

Top-right:
- LinkedIn icon
- GitHub icon
- Instagram icon

Requirements:
- Clicking a menu item scrolls to the corresponding section.
- Active navigation item should be highlighted.
- Responsive mobile navigation.
- Smooth scrolling.
- Resume button should open or download the uploaded resume.

---

# 4. HOME / HERO SECTION

Create a two-column hero layout.

LEFT SIDE:
- Large profile photograph.
- Rounded corners.
- Professional appearance.
- Image should be replaceable through the admin dashboard.

RIGHT SIDE:

Heading:
"Hi, I'm Bichu Biju"

Professional title:
"AI/ML Enthusiast"

Introduction:
"I'm a Computer Science Engineering student passionate about Artificial Intelligence, Machine Learning, software development, and building innovative technology solutions. I enjoy exploring new technologies, solving real-world problems, and transforming creative ideas into practical applications."

Buttons:
- LinkedIn
- View Projects
- Download Resume

Add small engineering-related illustrations around the hero section:
- Artificial intelligence illustrations.
- Neural network diagrams.
- Computer science sketches.
- Machine learning-related illustrations.

Make the entire hero section editable through the admin dashboard.

---

# 5. ABOUT ME SECTION

Create a professional About Me section.

Include:
- Profile photograph.
- Full name.
- Professional title.
- Short biography.
- Educational background.
- Career interests.
- Personal interests.
- Current learning goals.

Add a timeline-style layout for important milestones.

All content must be editable through the admin dashboard.

---

# 6. SKILLS SECTION

Create a modern skills section with categorized skill cards.

Categories:

Programming Languages:
- Python
- Java
- C
- C++

AI / Machine Learning:
- Machine Learning
- Deep Learning
- Artificial Intelligence
- Data Science
- NLP

Web Development:
- HTML
- CSS
- JavaScript
- Django

Tools and Technologies:
- Git
- GitHub
- VS Code
- Jupyter Notebook
- Supabase

Requirements:
- Skill icons.
- Skill categories.
- Optional proficiency indicators.
- Add, edit, and delete skills from admin.
- Ability to reorder skills.
- Display skills dynamically from the database.

Do not hardcode the skills.

---

# 7. PROJECTS SECTION

Create a visually attractive project showcase.

Each project card must contain:

- Project thumbnail.
- Project title.
- Short description.
- Technologies used.
- Project category.
- GitHub repository link.
- Live demo link.
- Project details button.

Project categories:
- Artificial Intelligence
- Machine Learning
- Web Development
- Python Development
- Other Engineering Projects

Project details page:
When visitors click a project, display:
- Project title.
- Large project image.
- Detailed description.
- Problem statement.
- Proposed solution.
- Technologies used.
- Key features.
- Screenshots.
- GitHub link.
- Live demo link.

Admin functionality:
- Create new projects.
- Edit existing projects.
- Delete projects.
- Upload project thumbnails.
- Upload multiple screenshots.
- Add GitHub URLs.
- Add live demo URLs.
- Mark featured projects.
- Publish or unpublish projects.

All project information must come from Supabase PostgreSQL through Django APIs.

---

# 8. EDUCATION SECTION

Create an education timeline.

Display:
- Institution name.
- Degree.
- Department.
- Specialization.
- Starting year.
- Graduation year.
- Academic information.

Provide admin controls to add, update, and delete education records.

---

# 9. CERTIFICATIONS AND ACHIEVEMENTS

Create a certification gallery.

Each certification should contain:
- Certificate image.
- Certificate name.
- Issuing organization.
- Issue date.
- Credential URL.

Achievements section:
- Hackathons.
- Technical competitions.
- Academic achievements.
- Workshops.
- Internships.

Admin must be able to upload certificate images and manage all records.

---

# 10. RESUME SECTION

Create a dedicated resume section.

Features:
- Resume preview.
- Download resume button.
- Upload new PDF resume.
- Replace old resume.
- Display last updated date.

The administrator must be able to replace the resume through the admin dashboard.

Store resume files securely using Supabase Storage.

---

# 11. CONTACT SECTION

Create a modern contact section.

Display:
- Email address.
- LinkedIn profile.
- GitHub profile.
- Instagram profile.
- Location.

Create a contact form with:
- Full name.
- Email address.
- Subject.
- Message.
- Submit button.

Backend functionality:
- Validate submitted information.
- Store messages in PostgreSQL.
- Display success and error messages.
- Prevent spam using rate limiting and server-side validation.

Admin functionality:
- View contact messages.
- Read individual messages.
- Mark messages as read or unread.
- Delete messages.

---

# 12. ASK ME ANYTHING SECTION

Create a unique interactive section titled:

"Ask Me Anything"

Visitors can submit questions about:
- My projects.
- My technical skills.
- My engineering journey.
- AI and machine learning.
- Collaboration opportunities.

Features:
- Question input field.
- Submit button.
- Store questions in PostgreSQL.
- Admin can view questions.
- Admin can write answers.
- Admin can publish answers publicly.

Do not expose private questions or administrator information.

---

# 13. ADMIN DASHBOARD

This is one of the most important features.

Create a separate, secure admin panel.

Admin URL:
/admin-dashboard/

Login page:
/admin-dashboard/login/

Only authorized administrators should access this dashboard.

Design:
- Modern dashboard UI.
- Sidebar navigation.
- Top navigation bar.
- Statistics cards.
- Tables.
- Forms.
- Search and filtering.
- Responsive layout.

Dashboard sidebar:

1. Dashboard Overview
2. Profile Management
3. About Me
4. Skills Management
5. Projects Management
6. Education Management
7. Certifications
8. Achievements
9. Resume Management
10. Contact Messages
11. Visitor Questions
12. Social Media Links
13. Website Settings
14. Change Password
15. Logout

---

# 14. ADMIN DASHBOARD FUNCTIONALITIES

A. PROFILE MANAGEMENT

Admin can edit:
- Full name.
- Profile image.
- Professional title.
- Introduction.
- Biography.
- Email.
- Location.
- LinkedIn URL.
- GitHub URL.
- Instagram URL.

B. SKILLS MANAGEMENT

Admin can:
- Add skills.
- Edit skills.
- Delete skills.
- Upload skill icons.
- Change skill categories.
- Update proficiency levels.
- Change display order.

C. PROJECT MANAGEMENT

Admin can:
- Add projects.
- Edit projects.
- Delete projects.
- Upload images.
- Upload screenshots.
- Add descriptions.
- Add technologies.
- Add GitHub links.
- Add live demo links.
- Publish/unpublish projects.

D. EDUCATION MANAGEMENT

Admin can:
- Add education.
- Edit education.
- Delete education.
- Update institution information.
- Update academic years.

E. CERTIFICATION MANAGEMENT

Admin can:
- Upload certificates.
- Edit certificate details.
- Delete certificates.
- Add credential links.

F. RESUME MANAGEMENT

Admin can:
- Upload resume PDF.
- Replace existing resume.
- Delete outdated resume.
- Update resume description.

G. CONTACT MANAGEMENT

Admin can:
- View messages.
- Search messages.
- Mark messages as read.
- Delete messages.

H. WEBSITE SETTINGS

Admin can:
- Change website title.
- Update favicon.
- Change social links.
- Update contact information.
- Manage footer text.
- Enable or disable sections.

All admin modifications must immediately update the public portfolio after successful saving.

---

# 15. DATABASE DESIGN – SUPABASE POSTGRESQL
connection string = psql -h db.fkvqjpofyydjetrbbblw.supabase.co -p 5432 -d postgres -U postgres
host=db.fkvqjpofyydjetrbbblw.supabase.co
port=5432
database=postgres
user=postgres
. Configure Django
Install the required packages:
pip install django
pip install djangorestframework
pip install psycopg[binary]
pip install dj-database-url
pip install python-dotenv
pip install supabase

Create the following Django models:

1. Profile
   - id
   - full_name
   - professional_title
   - profile_image
   - introduction
   - biography
   - email
   - location
   - linkedin_url
   - github_url
   - instagram_url

2. Skill
   - id
   - name
   - category
   - icon
   - proficiency
   - display_order

3. Project
   - id
   - title
   - slug
   - description
   - detailed_description
   - category
   - thumbnail
   - technologies
   - github_url
   - live_demo_url
   - featured
   - is_published
   - created_at

4. ProjectImage
   - id
   - project_id
   - image
   - caption

5. Education
   - id
   - institution
   - degree
   - department
   - specialization
   - start_year
   - end_year
   - description

6. Certification
   - id
   - title
   - organization
   - certificate_image
   - issue_date
   - credential_url

7. Achievement
   - id
   - title
   - description
   - achievement_date
   - image

8. Resume
   - id
   - file
   - description
   - uploaded_at
   - is_active

9. ContactMessage
   - id
   - name
   - email
   - subject
   - message
   - is_read
   - created_at

10. VisitorQuestion
    - id
    - name
    - email
    - question
    - answer
    - is_published
    - created_at

11. WebsiteSettings
    - id
    - website_title
    - favicon
    - footer_text
    - contact_email
    - social_links

Use appropriate relationships, validation, indexes, and timestamps.

Use Django's built-in authentication system for administrator accounts.

---

# 16. BACKEND API STRUCTURE

Build REST APIs using Django REST Framework.

Suggested endpoints:

PROFILE:
GET /api/profile/
PUT /api/admin/profile/

SKILLS:
GET /api/skills/
POST /api/admin/skills/
PUT /api/admin/skills/{id}/
DELETE /api/admin/skills/{id}/

PROJECTS:
GET /api/projects/
GET /api/projects/{slug}/
POST /api/admin/projects/
PUT /api/admin/projects/{id}/
DELETE /api/admin/projects/{id}/

EDUCATION:
GET /api/education/
POST /api/admin/education/

CERTIFICATIONS:
GET /api/certifications/
POST /api/admin/certifications/

CONTACT:
POST /api/contact/
GET /api/admin/messages/

QUESTIONS:
POST /api/questions/
GET /api/admin/questions/

RESUME:
GET /api/resume/
POST /api/admin/resume/

Implement authentication, authorization, validation, pagination, and error handling.

All admin APIs must require authentication and appropriate permissions.

---

# 17. SECURITY REQUIREMENTS

Security is extremely important.

Implement:
- Django authentication.
- Secure admin login.
- Strong password hashing.
- CSRF protection.
- XSS protection.
- SQL injection protection through Django ORM.
- Server-side input validation.
- Secure file uploads.
- File type and size validation.
- Environment variable configuration.
- HTTPS in production.
- API permission controls.
- Login rate limiting.
- Secure session management.

Never expose:
- Django SECRET_KEY.
- Database passwords.
- Supabase service-role keys.
- Admin credentials.

Do not use Supabase service-role keys in browser-side JavaScript.

---

# 18. RESPONSIVE DESIGN

The website must work perfectly on:

- Desktop computers.
- Laptops.
- Tablets.
- Android phones.
- iPhones.

Mobile requirements:
- Hamburger navigation.
- Responsive project cards.
- Properly scaled profile image.
- Touch-friendly buttons.
- Responsive admin dashboard.
- No horizontal scrolling.

---

# 19. ANIMATIONS AND INTERACTIONS

Implement:
- Smooth scrolling.
- Fade-in animations.
- Scroll-triggered section animations.
- Hover effects on project cards.
- Button transitions.
- Animated navigation indicator.
- Image hover effects.
- Loading indicators.
- Form submission feedback.

Keep animations lightweight and professional.

Respect reduced-motion accessibility preferences.

---

# 20. SEO AND PERFORMANCE

Implement:
- SEO-friendly page titles.
- Meta descriptions.
- Open Graph metadata.
- Semantic HTML.
- Image optimization.
- Lazy loading.
- Sitemap.
- Robots.txt.
- Clean project URLs.
- Accessibility improvements.

---

# 21. PROJECT STRUCTURE

Organize the Django project professionally.

Suggested structure:

portfolio/
│
├── backend/
│   ├── config/
│   ├── accounts/
│   ├── profiles/
│   ├── projects/
│   ├── skills/
│   ├── education/
│   ├── certifications/
│   ├── contact/
│   ├── questions/
│   ├── requirements.txt
│   └── manage.py
│
├── frontend/
│   ├── templates/
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   ├── images/
│   │   └── icons/
│   └── components/
│
├── .env.example
├── .gitignore
└── README.md

---

# 22. DEPLOYMENT

Prepare the application for production deployment.

Backend:
- Deploy Django using a suitable Python hosting provider.

Database:
- Supabase PostgreSQL.

Storage:
- Supabase Storage.

Frontend:
- Serve through Django templates or a properly configured frontend deployment.

Provide:
- Environment variable configuration.
- Database migration instructions.
- Static file configuration.
- Production settings.
- Deployment instructions.
- Admin account creation instructions.

---

# 23. IMPORTANT DEVELOPMENT INSTRUCTIONS

Follow these rules while building:

1. First build the complete public portfolio UI.
2. Then implement the Django backend.
3. Configure Supabase PostgreSQL connection.
4. Create all database models and migrations.
5. Implement REST APIs.
6. Build the admin dashboard.
7. Connect all frontend sections to backend APIs.
8. Test all CRUD operations.
9. Test image and PDF uploads.
10. Test admin authentication and authorization.
11. Test responsive layouts.
12. Fix all errors before considering the project complete.

Do not create dummy buttons that do nothing.

Do not hardcode dynamic content.

Do not use localStorage as the primary database.

Do not leave the admin dashboard as a static mockup.

All profile, project, skill, education, certification, resume, and website settings must be dynamically manageable through the admin dashboard.

---

# FINAL EXPECTED RESULT

Deliver a complete, working, full-stack personal engineering portfolio website for Bichu Biju.

The website should communicate the identity of an ambitious Computer Science Engineering student and AI/ML enthusiast.

The public portfolio should be clean, professional, minimal, and visually impressive.

The admin dashboard should make the website easy to maintain without programming knowledge.

The entire application must use Python Django as its backend and Supabase PostgreSQL as its database.

Provide complete source code, database configuration, installation instructions, and deployment documentation.