# Smart Recruitment System (Enterprise ATS)

Smart Recruitment System is a professional, production-style enterprise Applicant Tracking System (ATS) built with Python, Flask, SQLAlchemy ORM, Flask-Login, MySQL database support, and Bootstrap 5.

It provides a clean, minimal corporate user interface (Inter typography, enterprise color palette, rectangular subtle-radius controls) with zero flashy or distracting effects (no glassmorphism, no neumorphism, no heavy gradients).

---

## Tech Stack & Architecture

- **Frontend**: HTML5, CSS3 (Enterprise Custom Theme), Bootstrap 5.3.6, JavaScript (ES6)
- **Backend Framework**: Python 3.12+, Flask Framework
- **Database**: MySQL 8.0+ / SQLite fallback for instant local execution
- **ORM**: Flask-SQLAlchemy 3.1+
- **Authentication**: Flask-Login, Werkzeug Password Hashing
- **File Uploads**: Resume upload handler supporting PDF, DOC, DOCX up to 10 MB limit
- **Architecture**: MVC (Model-View-Controller) with RESTful routing

---

## Directory Structure

```
SmartRecruitmentSystem/
├── app.py                    # Main Flask application initialization & entrypoint
├── config.py                 # Configuration settings (Database, Secret Key, File Uploads)
├── models.py                 # SQLAlchemy ORM Models (User, Job, Application)
├── routes.py                 # RESTful route controllers & role authorization decorators
├── schema.sql                # Production MySQL database initialization script
├── seed.py                   # Helper script to populate demo accounts & job vacancies
├── requirements.txt          # Python package dependencies
├── README.md                 # Complete system documentation
├── uploads/
│   └── resumes/              # Secure directory for uploaded candidate resume files
├── static/
│   ├── css/
│   │   └── custom.css        # Enterprise corporate design system & custom styles
│   └── js/
│       └── main.js           # Client-side form validation, file checks, modal triggers
└── templates/
    ├── base.html             # Base HTML5 layout with enterprise navigation & flash alerts
    ├── home.html             # Public landing page (Hero, Overview, Features, How It Works)
    ├── login.html            # User authentication (Sign In)
    ├── register.html         # User registration (Role: Recruiter vs Candidate)
    ├── recruiter/
    │   ├── dashboard.html    # Recruiter analytics, metric cards, recent listings
    │   ├── post_job.html     # Create new job posting
    │   ├── edit_job.html     # Modify existing job listing
    │   ├── manage_jobs.html  # Table of posted jobs with status & action triggers
    │   ├── view_applications.html # Review candidates, preview resumes, update status
    │   └── profile.html      # Recruiter profile view & updates
    └── candidate/
        ├── dashboard.html    # Candidate metrics, application stats, completion progress
        ├── browse_jobs.html  # Job search with multi-faceted filtering (Location, Type, Company)
        ├── job_details.html  # Complete job description page with direct apply trigger
        ├── apply_job.html    # Resume upload & application submission
        ├── my_applications.html # Real-time application tracking table with status badges
        └── profile.html      # Candidate profile editor (Skills, Education, Experience, Resume)
```

---

## Installation & Setup Instructions

### 1. Prerequisites
- Python 3.10+ installed on system
- MySQL Server (Optional: If MySQL is not running locally, the system automatically falls back to an embedded SQLite database `smart_recruitment.db` for instant out-of-the-box execution).

### 2. Clone / Navigate to Project Directory
```bash
cd SmartRecruitmentSystem
```

### 3. Create Virtual Environment & Install Dependencies
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment (Windows)
venv\Scripts\activate

# Install required packages
pip install -r requirements.txt
```

### 4. Database Setup

#### Option A: Automatic Local Execution (SQLite Fallback)
No database configuration needed! Simply running `python app.py` or `python seed.py` will automatically create the database tables.

#### Option B: MySQL Configuration
To connect to a live MySQL server:
1. Run the included `schema.sql` script in MySQL Workbench or terminal:
   ```bash
   mysql -u root -p < schema.sql
   ```
2. Set environment variables or configure your MySQL credentials in `config.py`:
   ```bash
   set MYSQL_USER=root
   set MYSQL_PASSWORD=yourpassword
   set MYSQL_HOST=localhost
   set MYSQL_DB=smart_recruitment_db
   ```

### 5. Seed Demo Data
Populate demo recruiter accounts, candidate accounts, and job postings:
```bash
python seed.py
```

### 6. Launch Application Server
```bash
python app.py
```
Open your browser and navigate to: **`http://127.0.0.1:5000`**

---

## Pre-seeded Credentials for Instant Testing

| Role | Email | Password |
|---|---|---|
| **Recruiter** | `recruiter@example.com` | `password123` |
| **Candidate** | `candidate@example.com` | `password123` |
| **Candidate 2** | `john.smith@example.com` | `password123` |

---

## Key System Features

### Recruiter Module
- **Dashboard**: High-level metric cards showing total jobs posted, total applications, pending candidate reviews, and shortlisted candidates.
- **Job Management**: Create, edit, and delete job postings with fields for title, company, location, employment type, salary, experience, required skills, detailed description, and application deadline.
- **Application Management**: Filter applicants by job posting and status (Pending, Shortlisted, Selected, Rejected). Inspect applicant details and preview uploaded PDF/DOCX resumes in the browser.
- **Status Updates**: Update application status with instant badge reflection for candidates.

### Candidate Module
- **Dashboard**: Track available jobs, submitted applications, shortlisted count, and profile completion percentage.
- **Job Search & Filters**: Multi-faceted filter engine supporting keyword search (title, company, skills), location dropdown, employment type dropdown, and company dropdown.
- **Resume Upload & Apply**: Apply for job openings with automatic profile resume attachment or custom resume upload (PDF/DOCX up to 10 MB).
- **Application Tracking**: Monitor real-time status updates (Pending, Shortlisted, Selected, Rejected) for all submitted applications.
- **Candidate Profile**: Edit personal details, contact info, technical skills, education history, work experience, and default resume file.

---

## Security Features
- Secure Password Hashing using `werkzeug.security` (PBKDF2/SHA256).
- SQL Injection protection via SQLAlchemy ORM.
- Role-based Access Control via custom Flask route decorators (`@recruiter_required`, `@candidate_required`).
- File Upload Validation restricting formats to PDF, DOC, DOCX and setting maximum content length (10 MB). Filenames are sanitized with `secure_filename` and unique timestamp prefixes.
"# smart_recruitment_system" 
"# smart_recruitment_system" 
