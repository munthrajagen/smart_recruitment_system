import os
from datetime import date, datetime, timedelta
from app import create_app
from models import db, User, Job, Application

app = create_app()

def create_sample_resumes(upload_folder):
    os.makedirs(upload_folder, exist_ok=True)
    resumes_content = {
        "resume_alex_rivera.pdf": """ALEX RIVERA - FULL STACK SOFTWARE ENGINEER
Email: candidate@example.com | Phone: +1 (555) 987-6543 | Location: Austin, TX

SUMMARY:
Results-driven Full Stack Software Engineer with 2+ years of experience building responsive enterprise web applications using Python, Flask, MySQL, REST APIs, and modern JavaScript frontend frameworks.

TECHNICAL SKILLS:
- Languages: Python, JavaScript (ES6+), SQL, HTML5, CSS3
- Frameworks & Libraries: Flask, SQLAlchemy, Bootstrap 5, Jinja2, React
- Databases & Tools: MySQL, SQLite, Git, Docker, Postman, Linux

WORK EXPERIENCE:
CloudDevs LLC - Full Stack Web Developer (2024 - Present)
- Developed and deployed high-performance RESTful APIs servicing over 50k active monthly users.
- Designed database schemas and managed ORM migrations using SQLAlchemy.
- Built clean, accessible UI components with Bootstrap 5 and custom CSS systems.

EDUCATION:
B.S. in Software Engineering, UT Austin (2020 - 2024)
""",
        "resume_john_smith.pdf": """JOHN SMITH - SENIOR DATA ANALYST & BI SPECIALIST
Email: john.smith@example.com | Phone: +1 (555) 345-6789 | Location: New York, NY

SUMMARY:
Data Analyst with 3+ years of experience in data visualization, SQL query optimization, statistical modeling, and business intelligence reporting.

TECHNICAL SKILLS:
- Data Analysis: SQL, Python (Pandas, NumPy), Excel (VBA)
- Business Intelligence: Tableau, Power BI, Looker
- Databases: MySQL, PostgreSQL, Snowflake

WORK EXPERIENCE:
FinTech Analytics - BI Analyst (2023 - Present)
- Created automated executive dashboards reducing manual reporting time by 40%.
- Conducted exploratory data analysis on consumer transaction datasets.

EDUCATION:
M.S. in Data Science, Columbia University (2021 - 2023)
""",
        "resume_david_miller.pdf": """DAVID MILLER - DEVOPS & CLOUD ENGINEER
Email: david.miller@example.com | Phone: +1 (555) 456-7890 | Location: San Francisco, CA

SUMMARY:
DevOps Engineer specializing in AWS cloud infrastructure, CI/CD pipeline automation, Docker containerization, and Kubernetes cluster administration.

TECHNICAL SKILLS:
- Cloud Platforms: AWS (EC2, S3, RDS, Lambda), GCP
- DevOps & Tools: Docker, Kubernetes, Terraform, Jenkins, Git, Linux, Shell Scripting

WORK EXPERIENCE:
ScaleCloud Systems - DevOps Infrastructure Engineer (2023 - Present)
- Architected automated CI/CD deployment pipelines cutting build times by 50%.

EDUCATION:
B.S. in Computer Science, UC Berkeley (2019 - 2023)
""",
        "resume_emily_watson.pdf": """EMILY WATSON - SENIOR PRODUCT MANAGER
Email: emily.watson@example.com | Phone: +1 (555) 567-8901 | Location: Chicago, IL

SUMMARY:
Product Manager with 4+ years leading agile software teams, gathering user feedback, defining product roadmaps, and executing enterprise ATS solutions.

SKILLS:
- Product Strategy, User Experience Research, Agile/Scrum, Roadmap Planning, Data Analytics

EDUCATION:
B.A. in Business Administration, Northwestern University
""",
        "resume_robert_chen.pdf": """ROBERT CHEN - FRONTEND DEVELOPER
Email: robert.chen@example.com | Phone: +1 (555) 678-9012 | Location: Seattle, WA

SUMMARY:
Frontend Engineer with 3 years experience building responsive, intuitive web interfaces with HTML5, CSS3, JavaScript ES6, React, and Bootstrap.

TECHNICAL SKILLS:
- JavaScript (ES6+), HTML5, CSS3, React, Vue.js, Bootstrap 5, Webpack
"""
    }

    for filename, content in resumes_content.items():
        filepath = os.path.join(upload_folder, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

def seed_database():
    app = create_app()
    with app.app_context():
        print("Recreating database tables for seed execution...")
        db.drop_all()
        db.create_all()

        upload_folder = app.config['UPLOAD_FOLDER']
        create_sample_resumes(upload_folder)

        # 1. Seed Recruiters
        recruiter1 = User(
            full_name='Sarah Jenkins',
            email='recruiter@example.com',
            role='recruiter',
            company_name='ABC Technologies',
            company_description='ABC Technologies is a leading software company specializing in enterprise software development, ATS systems, and cloud solutions.',
            company_location='Chennai',
            company_website='www.abctechnologies.com',
            phone='+1 (555) 234-5678',
            address='100 Corporate Way, Suite 500, Chennai, India'
        )
        recruiter1.set_password('password123')
        db.session.add(recruiter1)

        recruiter2 = User(
            full_name='Michael Vance',
            email='recruiter2@example.com',
            role='recruiter',
            company_name='XYZ Solutions',
            company_description='XYZ Solutions delivers high-throughput data analytics, machine learning tools, and business intelligence platforms.',
            company_location='Bangalore',
            company_website='www.xyzsolutions.com',
            phone='+1 (555) 876-5432',
            address='200 Tech Park, Bangalore, India'
        )
        recruiter2.set_password('password123')
        db.session.add(recruiter2)

        recruiter3 = User(
            full_name='David Harris',
            email='recruiter3@example.com',
            role='recruiter',
            company_name='Acme Innovations',
            company_description='Acme Innovations builds next-generation SaaS product management and recruitment technology.',
            company_location='Mumbai',
            company_website='www.acmeinnovations.com',
            phone='+1 (555) 999-1111',
            address='500 Tech Hub, Mumbai, India'
        )
        recruiter3.set_password('password123')
        db.session.add(recruiter3)

        # 2. Seed Candidates with uploaded resume paths
        candidate1 = User(
            full_name='Alex Rivera',
            email='candidate@example.com',
            role='candidate',
            phone='+1 (555) 987-6543',
            address='42 Innovation Boulevard, Austin, TX',
            skills='Python, Flask, MySQL, JavaScript, HTML5, CSS3, REST APIs',
            education='B.S. in Software Engineering, UT Austin (2020-2024)',
            experience='2 years as Full Stack Web Developer at CloudDevs LLC',
            resume_path='resume_alex_rivera.pdf'
        )
        candidate1.set_password('password123')
        db.session.add(candidate1)

        candidate2 = User(
            full_name='John Smith',
            email='john.smith@example.com',
            role='candidate',
            phone='+1 (555) 345-6789',
            address='128 Park Avenue, New York, NY',
            skills='Data Analysis, Python, SQL, Tableau, Power BI, Excel',
            education='M.S. in Data Science, Columbia University',
            experience='3 years as Business Intelligence Analyst',
            resume_path='resume_john_smith.pdf'
        )
        candidate2.set_password('password123')
        db.session.add(candidate2)

        candidate3 = User(
            full_name='David Miller',
            email='david.miller@example.com',
            role='candidate',
            phone='+1 (555) 456-7890',
            address='74 Cloud Way, San Francisco, CA',
            skills='AWS, Docker, Kubernetes, Terraform, Linux, CI/CD, Python',
            education='B.S. in Computer Science, UC Berkeley (2019-2023)',
            experience='3 years as DevOps Infrastructure Engineer',
            resume_path='resume_david_miller.pdf'
        )
        candidate3.set_password('password123')
        db.session.add(candidate3)

        candidate4 = User(
            full_name='Emily Watson',
            email='emily.watson@example.com',
            role='candidate',
            phone='+1 (555) 567-8901',
            address='15 Lakefront Drive, Chicago, IL',
            skills='Product Management, Agile/Scrum, Roadmap Planning, UX Research, Jira',
            education='B.A. in Business Administration, Northwestern University',
            experience='4 years as Product Manager at TechSoft',
            resume_path='resume_emily_watson.pdf'
        )
        candidate4.set_password('password123')
        db.session.add(candidate4)

        candidate5 = User(
            full_name='Robert Chen',
            email='robert.chen@example.com',
            role='candidate',
            phone='+1 (555) 678-9012',
            address='88 Tech Pine Road, Seattle, WA',
            skills='JavaScript, React, Vue.js, HTML5, CSS3, Bootstrap 5, Webpack',
            education='B.S. in Information Systems, University of Washington',
            experience='3 years as Frontend Developer',
            resume_path='resume_robert_chen.pdf'
        )
        candidate5.set_password('password123')
        db.session.add(candidate5)

        db.session.commit()

        # 3. Seed Jobs
        today = date.today()
        
        job1 = Job(
            recruiter_id=recruiter1.id,
            title="Python Developer",
            company=recruiter1.company_name,
            location="Chennai",
            employment_type="Full-Time",
            salary="₹6,00,000 - ₹10,00,000 / year",
            experience="2-4 Years",
            skills="Python, Flask, SQL, REST APIs, Git",
            description="ABC Technologies is looking for a Python developer to build web applications, design database schemas, and integrate REST APIs for enterprise applications.",
            last_date=today + timedelta(days=30),
            openings=3,
            is_active=True
        )
        db.session.add(job1)

        job2 = Job(
            recruiter_id=recruiter1.id,
            title="Senior Full Stack Engineer",
            company=recruiter1.company_name,
            location="Remote",
            employment_type="Full-Time",
            salary="₹12,00,000 - ₹18,00,000 / year",
            experience="4-6 Years",
            skills="Python, Flask, React, MySQL, AWS, Microservices",
            description="Join ABC Technologies to architect enterprise cloud application suites and mentor software development teams.",
            last_date=today + timedelta(days=45),
            openings=2,
            is_active=True
        )
        db.session.add(job2)

        job3 = Job(
            recruiter_id=recruiter2.id,
            title="Data Analyst",
            company=recruiter2.company_name,
            location="Bangalore",
            employment_type="Full-Time",
            salary="₹5,00,000 - ₹8,00,000 / year",
            experience="1-3 Years",
            skills="SQL, Python, Pandas, Tableau, Power BI, MySQL",
            description="XYZ Solutions is seeking a Data Analyst to transform complex datasets into executive dashboards and insights.",
            last_date=today + timedelta(days=25),
            openings=2,
            is_active=True
        )
        db.session.add(job3)

        job4 = Job(
            recruiter_id=recruiter2.id,
            title="Cloud DevOps Engineer",
            company=recruiter2.company_name,
            location="Hyderabad",
            employment_type="Contract",
            salary="₹8,00,000 - ₹14,00,000 / year",
            experience="3-5 Years",
            skills="Docker, Kubernetes, AWS, Terraform, CI/CD pipelines",
            description="XYZ Solutions is hiring a DevOps Engineer to manage container orchestrations and automate cloud deployment pipelines.",
            last_date=today + timedelta(days=20),
            openings=1,
            is_active=True
        )
        db.session.add(job4)

        job5 = Job(
            recruiter_id=recruiter3.id,
            title="Technical Product Manager",
            company=recruiter3.company_name,
            location="Mumbai",
            employment_type="Full-Time",
            salary="₹15,00,000 - ₹22,00,000 / year",
            experience="4-7 Years",
            skills="Product Roadmap, Agile, User Stories, Data Analytics, JIRA",
            description="Acme Innovations is looking for a Product Manager to lead feature strategy, agile sprint planning, and user feedback cycles.",
            last_date=today + timedelta(days=35),
            openings=1,
            is_active=True
        )
        db.session.add(job5)

        db.session.commit()

        # 4. Seed Applications with diverse workflow statuses & rejection reasons
        applications_data = [
            # Job 1 (Python Developer - ABC Tech)
            {"candidate": candidate1, "job": job1, "resume": "resume_alex_rivera.pdf", "status": "Applied", "reason": None},
            {"candidate": candidate3, "job": job1, "resume": "resume_david_miller.pdf", "status": "Shortlisted", "reason": None},
            {"candidate": candidate5, "job": job1, "resume": "resume_robert_chen.pdf", "status": "Interview", "reason": None},
            
            # Job 2 (Senior Full Stack Engineer - ABC Tech)
            {"candidate": candidate1, "job": job2, "resume": "resume_alex_rivera.pdf", "status": "Under Review", "reason": None},
            {"candidate": candidate5, "job": job2, "resume": "resume_robert_chen.pdf", "status": "Selected", "reason": None},

            # Job 3 (Data Analyst - XYZ Solutions)
            {"candidate": candidate2, "job": job3, "resume": "resume_john_smith.pdf", "status": "Selected", "reason": None},
            {"candidate": candidate1, "job": job3, "resume": "resume_alex_rivera.pdf", "status": "Rejected", "reason": "Candidate skill set is primarily software development rather than statistics and BI analytics."},

            # Job 4 (Cloud DevOps - XYZ Solutions)
            {"candidate": candidate3, "job": job4, "resume": "resume_david_miller.pdf", "status": "Interview", "reason": None},
            {"candidate": candidate2, "job": job4, "resume": "resume_john_smith.pdf", "status": "Rejected", "reason": "Required experience in AWS and Docker does not match applicant profile."},

            # Job 5 (Product Manager - Acme Innovations)
            {"candidate": candidate4, "job": job5, "resume": "resume_emily_watson.pdf", "status": "Shortlisted", "reason": None}
        ]

        for app_info in applications_data:
            app = Application(
                candidate_id=app_info["candidate"].id,
                job_id=app_info["job"].id,
                resume=app_info["resume"],
                status=app_info["status"],
                rejection_reason=app_info["reason"]
            )
            db.session.add(app)

        db.session.commit()

        print("----------------------------------------------------------------------")
        print("Database & Sample Resumes populated successfully!")
        print("----------------------------------------------------------------------")
        print("RECRUITER ACCOUNTS:")
        print("1. recruiter@example.com   / password123 (ABC Technologies)")
        print("2. recruiter2@example.com  / password123 (XYZ Solutions)")
        print("3. recruiter3@example.com  / password123 (Acme Innovations)")
        print("\nCANDIDATE ACCOUNTS:")
        print("1. candidate@example.com     / password123 (Alex Rivera)")
        print("2. john.smith@example.com    / password123 (John Smith)")
        print("3. david.miller@example.com  / password123 (David Miller)")
        print("4. emily.watson@example.com  / password123 (Emily Watson)")
        print("5. robert.chen@example.com   / password123 (Robert Chen)")
        print("----------------------------------------------------------------------")

if __name__ == '__main__':
    seed_database()
