from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'recruiter' or 'candidate'
    
    # Recruiter Company Profile fields
    company_name = db.Column(db.String(200), nullable=True)
    company_description = db.Column(db.Text, nullable=True)
    company_location = db.Column(db.String(200), nullable=True)
    company_website = db.Column(db.String(300), nullable=True)
    
    # Profile fields (mainly for Candidate, optional for Recruiter)
    phone = db.Column(db.String(20), nullable=True)
    address = db.Column(db.String(255), nullable=True)
    skills = db.Column(db.Text, nullable=True)
    education = db.Column(db.Text, nullable=True)
    experience = db.Column(db.Text, nullable=True)
    resume_path = db.Column(db.String(255), nullable=True)
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    posted_jobs = db.relationship('Job', backref='recruiter', lazy=True, cascade="all, delete-orphan")
    applications = db.relationship('Application', backref='candidate', lazy=True, cascade="all, delete-orphan")

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_recruiter(self):
        return self.role == 'recruiter'

    @property
    def is_candidate(self):
        return self.role == 'candidate'

    def __repr__(self):
        return f'<User {self.email} ({self.role})>'


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    title = db.Column(db.String(150), nullable=False)
    company = db.Column(db.String(150), nullable=False)
    location = db.Column(db.String(100), nullable=False)
    employment_type = db.Column(db.String(50), nullable=False)  # e.g., Full-time, Part-time, Contract, Remote, Internship
    salary = db.Column(db.String(100), nullable=False)
    experience = db.Column(db.String(50), nullable=False)
    skills = db.Column(db.Text, nullable=False)
    description = db.Column(db.Text, nullable=False)
    last_date = db.Column(db.Date, nullable=False)
    openings = db.Column(db.Integer, default=1, nullable=False)
    is_active = db.Column(db.Boolean, default=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    applications = db.relationship('Application', backref='job', lazy=True, cascade="all, delete-orphan")

    @property
    def display_company(self):
        if self.recruiter and self.recruiter.company_name:
            return self.recruiter.company_name
        return self.company

    def __repr__(self):
        return f'<Job {self.title} at {self.company}>'


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    candidate_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id', ondelete='CASCADE'), nullable=False)
    resume = db.Column(db.String(255), nullable=False)
    status = db.Column(db.String(30), default='Applied', nullable=False)  # 'Applied', 'Under Review', 'Shortlisted', 'Interview', 'Selected', 'Rejected'
    rejection_reason = db.Column(db.Text, nullable=True)
    applied_date = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    __table_args__ = (
        db.UniqueConstraint('candidate_id', 'job_id', name='unique_candidate_job_application'),
    )

    def __repr__(self):
        return f'<Application Candidate:{self.candidate_id} Job:{self.job_id} Status:{self.status}>'
