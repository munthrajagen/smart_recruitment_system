import os
from datetime import date, datetime, timedelta
from app import create_app
from models import db, User, Job, Application

app = create_app()

def seed_database():
    with app.app_context():
        print("Recreating database tables for seed execution...")
        db.create_all()

        # 1. Seed Recruiter Account
        recruiter = User.query.filter_by(email='recruiter@example.com').first()
        if not recruiter:
            recruiter = User(
                full_name='Sarah Jenkins',
                email='recruiter@example.com',
                role='recruiter',
                phone='+1 (555) 234-5678',
                address='100 Corporate Way, Tech Suite 500, San Francisco, CA'
            )
            recruiter.set_password('password123')
            db.session.add(recruiter)
            print("Created Recruiter: recruiter@example.com (Password: password123)")
        
        # 2. Seed Candidate Account
        candidate = User.query.filter_by(email='candidate@example.com').first()
        if not candidate:
            candidate = User(
                full_name='Alex Rivera',
                email='candidate@example.com',
                role='candidate',
                phone='+1 (555) 987-6543',
                address='42 Innovation Boulevard, Austin, TX',
                skills='Python, Flask, MySQL, JavaScript, HTML5, CSS3, REST APIs',
                education='B.S. in Software Engineering, UT Austin (2020-2024)',
                experience='2 years as Full Stack Web Developer at CloudDevs LLC'
            )
            candidate.set_password('password123')
            db.session.add(candidate)
            print("Created Candidate: candidate@example.com (Password: password123)")

        # 3. Second Candidate
        candidate2 = User.query.filter_by(email='john.smith@example.com').first()
        if not candidate2:
            candidate2 = User(
                full_name='John Smith',
                email='john.smith@example.com',
                role='candidate',
                phone='+1 (555) 345-6789',
                address='128 Park Avenue, New York, NY',
                skills='Data Analysis, Python, SQL, Tableau, Power BI, Excel',
                education='M.S. in Data Science, Columbia University',
                experience='3 years as Business Intelligence Analyst'
            )
            candidate2.set_password('password123')
            db.session.add(candidate2)

        db.session.commit()

        # 4. Seed Job Postings
        if Job.query.count() == 0:
            today = date.today()
            jobs_data = [
                {
                    "title": "Senior Full Stack Python Developer",
                    "company": "TechCorp Global",
                    "location": "San Francisco, CA (Hybrid)",
                    "employment_type": "Full-Time",
                    "salary": "$120,000 - $145,000 / year",
                    "experience": "4-6 Years",
                    "skills": "Python, Flask, Django, PostgreSQL, Vue.js / React, RESTful APIs, Git",
                    "description": "TechCorp Global is seeking an experienced Senior Full Stack Python Developer to build and maintain high-scale enterprise recruitment and web platforms.\n\nKey Responsibilities:\n- Architect modular RESTful APIs using Python Flask and SQLAlchemy ORM.\n- Collaborate with UI/UX engineers to implement responsive user interfaces.\n- Optimize database queries and ensure high availability and security compliance.\n- Mentor junior developers and participate in code reviews.",
                    "last_date": today + timedelta(days=30)
                },
                {
                    "title": "Data Analyst & Business Intelligence Specialist",
                    "company": "AnalyticsPro Solutions",
                    "location": "New York, NY (Remote)",
                    "employment_type": "Full-Time",
                    "salary": "$85,000 - $105,000 / year",
                    "experience": "2-4 Years",
                    "skills": "SQL, Python, Pandas, Tableau, PowerBI, MySQL, Data Warehousing",
                    "description": "We are hiring a Data Analyst to transform complex datasets into actionable executive insights.\n\nKey Responsibilities:\n- Write advanced SQL queries and build automated reporting dashboards.\n- Analyze recruitment and business metrics to improve conversion funnels.\n- Perform statistical analysis and work closely with product stakeholders.",
                    "last_date": today + timedelta(days=25)
                },
                {
                    "title": "Cloud DevOps & Infrastructure Engineer",
                    "company": "CloudScale Systems",
                    "location": "Austin, TX (Remote)",
                    "employment_type": "Contract",
                    "salary": "$70 - $90 / hour",
                    "experience": "3+ Years",
                    "skills": "Docker, Kubernetes, AWS, Linux, Terraform, CI/CD, Python",
                    "description": "CloudScale Systems is looking for a DevOps contractor to automate pipeline deployment and monitor cloud infrastructure health.",
                    "last_date": today + timedelta(days=15)
                },
                {
                    "title": "Associate UI/UX Frontend Developer",
                    "company": "Creative Enterprise Labs",
                    "location": "Chicago, IL (On-site)",
                    "employment_type": "Full-Time",
                    "salary": "$75,000 - $90,000 / year",
                    "experience": "1-3 Years",
                    "skills": "HTML5, CSS3, Bootstrap 5, JavaScript (ES6), Figma, Responsive Web Design",
                    "description": "Join our design engineering team to craft clean, corporate, high-usability web applications for enterprise clients.",
                    "last_date": today + timedelta(days=40)
                }
            ]

            for j_info in jobs_data:
                job = Job(
                    recruiter_id=recruiter.id,
                    title=j_info["title"],
                    company=j_info["company"],
                    location=j_info["location"],
                    employment_type=j_info["employment_type"],
                    salary=j_info["salary"],
                    experience=j_info["experience"],
                    skills=j_info["skills"],
                    description=j_info["description"],
                    last_date=j_info["last_date"]
                )
                db.session.add(job)
            
            db.session.commit()
            print("Successfully seeded initial job postings!")

        # 5. Seed Initial Sample Application
        if Application.query.count() == 0:
            first_job = Job.query.first()
            if first_job and candidate:
                app_sample = Application(
                    candidate_id=candidate.id,
                    job_id=first_job.id,
                    resume="sample_resume_alex.pdf",
                    status="Pending"
                )
                db.session.add(app_sample)
                db.session.commit()
                print("Seeded sample application for candidate Alex Rivera.")

        print("\nDatabase seeding completed successfully!")

if __name__ == '__main__':
    seed_database()
