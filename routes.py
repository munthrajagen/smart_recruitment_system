import os
import time
from functools import wraps
from datetime import datetime
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename

from models import db, User, Job, Application

main = Blueprint('main', __name__)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in current_app.config['ALLOWED_EXTENSIONS']

def recruiter_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_recruiter:
            flash('Access denied. Recruiter privileges required.', 'danger')
            return redirect(url_for('main.dashboard_redirect'))
        return f(*args, **kwargs)
    return decorated_function

def candidate_required(f):
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_candidate:
            flash('Access denied. Candidate privileges required.', 'danger')
            return redirect(url_for('main.dashboard_redirect'))
        return f(*args, **kwargs)
    return decorated_function

@main.route('/')
def home():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_redirect'))
    
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(6).all()
    total_jobs = Job.query.count()
    total_recruiters = User.query.filter_by(role='recruiter').count()
    total_candidates = User.query.filter_by(role='candidate').count()
    
    return render_template('home.html', 
                           recent_jobs=recent_jobs,
                           total_jobs=total_jobs,
                           total_recruiters=total_recruiters,
                           total_candidates=total_candidates)

@main.route('/dashboard')
@login_required
def dashboard_redirect():
    if current_user.is_recruiter:
        return redirect(url_for('main.recruiter_dashboard'))
    return redirect(url_for('main.candidate_dashboard'))

# -------------------------------------------------------------------
# AUTHENTICATION ROUTES
# -------------------------------------------------------------------

@main.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_redirect'))
        
    if request.method == 'POST':
        full_name = request.form.get('full_name', '').strip()
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
        role = request.form.get('role', 'candidate')
        company_name = request.form.get('company_name', '').strip()
        company_description = request.form.get('company_description', '').strip()
        company_location = request.form.get('company_location', '').strip()
        company_website = request.form.get('company_website', '').strip()

        if not full_name or not email or not password or not role:
            flash('Please fill in all required fields.', 'warning')
            return render_template('register.html')

        if role == 'recruiter' and (not company_name or not company_description):
            flash('Company Name and Company Description are required for Recruiter registration.', 'warning')
            return render_template('register.html')

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return render_template('register.html')

        if len(password) < 6:
            flash('Password must be at least 6 characters long.', 'warning')
            return render_template('register.html')

        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash('An account with this email address already exists.', 'danger')
            return render_template('register.html')

        user = User(
            full_name=full_name,
            email=email,
            role=role,
            company_name=company_name if role == 'recruiter' else None,
            company_description=company_description if role == 'recruiter' else None,
            company_location=company_location if role == 'recruiter' else None,
            company_website=company_website if role == 'recruiter' else None
        )
        user.set_password(password)

        db.session.add(user)
        db.session.commit()

        flash('Registration successful! Please sign in with your credentials.', 'success')
        return redirect(url_for('main.login'))

    return render_template('register.html')

@main.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('main.dashboard_redirect'))

    if request.method == 'POST':
        email = request.form.get('email', '').strip().lower()
        password = request.form.get('password', '')

        if not email or not password:
            flash('Please enter both email and password.', 'warning')
            return render_template('login.html')

        user = User.query.filter_by(email=email).first()

        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.full_name}!', 'success')
            next_page = request.args.get('next')
            if next_page:
                return redirect(next_page)
            return redirect(url_for('main.dashboard_redirect'))
        else:
            flash('Invalid email or password. Please try again.', 'danger')

    return render_template('login.html')

@main.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out successfully.', 'info')
    return redirect(url_for('main.home'))


# -------------------------------------------------------------------
# RECRUITER MODULE ROUTES
# -------------------------------------------------------------------

@main.route('/recruiter/dashboard')
@recruiter_required
def recruiter_dashboard():
    recruiter_id = current_user.id
    jobs = Job.query.filter_by(recruiter_id=recruiter_id).all()
    job_ids = [j.id for j in jobs]
    
    total_jobs = len(jobs)
    
    if job_ids:
        applications = Application.query.filter(Application.job_id.in_(job_ids)).all()
    else:
        applications = []
        
    total_applications = len(applications)
    pending_applications = sum(1 for a in applications if a.status == 'Pending')
    shortlisted_candidates = sum(1 for a in applications if a.status == 'Shortlisted')
    selected_candidates = sum(1 for a in applications if a.status == 'Selected')
    
    recent_jobs = Job.query.filter_by(recruiter_id=recruiter_id).order_by(Job.created_at.desc()).limit(5).all()
    
    return render_template('recruiter/dashboard.html',
                           total_jobs=total_jobs,
                           total_applications=total_applications,
                           pending_applications=pending_applications,
                           shortlisted_candidates=shortlisted_candidates,
                           selected_candidates=selected_candidates,
                           recent_jobs=recent_jobs)

@main.route('/recruiter/post-job', methods=['GET', 'POST'])
@recruiter_required
def post_job():
    if request.method == 'POST':
        title = request.form.get('title', '').strip()
        # Auto-set company from recruiter's profile, fallback to form input if provided
        company = current_user.company_name or request.form.get('company', '').strip()
        location = request.form.get('location', '').strip()
        employment_type = request.form.get('employment_type', 'Full-Time')
        salary = request.form.get('salary', '').strip()
        experience = request.form.get('experience', '').strip()
        skills = request.form.get('skills', '').strip()
        description = request.form.get('description', '').strip()
        last_date_str = request.form.get('last_date', '')
        openings = request.form.get('openings', 1, type=int)

        if not all([title, company, location, salary, experience, skills, description, last_date_str]):
            flash('All job fields are required.', 'warning')
            return render_template('recruiter/post_job.html')

        try:
            last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
        except ValueError:
            flash('Invalid date format. Please use YYYY-MM-DD.', 'danger')
            return render_template('recruiter/post_job.html')

        new_job = Job(
            recruiter_id=current_user.id,
            title=title,
            company=company,
            location=location,
            employment_type=employment_type,
            salary=salary,
            experience=experience,
            skills=skills,
            description=description,
            last_date=last_date,
            openings=openings,
            is_active=True
        )

        db.session.add(new_job)
        db.session.commit()

        flash('Job posted successfully!', 'success')
        return redirect(url_for('main.manage_jobs'))

    return render_template('recruiter/post_job.html')

@main.route('/recruiter/manage-jobs')
@recruiter_required
def manage_jobs():
    jobs = Job.query.filter_by(recruiter_id=current_user.id).order_by(Job.created_at.desc()).all()
    return render_template('recruiter/manage_jobs.html', jobs=jobs)

@main.route('/recruiter/toggle-job-status/<int:job_id>', methods=['POST'])
@recruiter_required
def toggle_job_status(job_id):
    job = Job.query.filter_by(id=job_id, recruiter_id=current_user.id).first_or_404()
    job.is_active = not job.is_active
    db.session.commit()
    status_str = "reopened" if job.is_active else "closed/deactivated"
    flash(f'Job "{job.title}" has been {status_str}.', 'success')
    return redirect(url_for('main.manage_jobs'))

@main.route('/recruiter/edit-job/<int:job_id>', methods=['GET', 'POST'])
@recruiter_required
def edit_job(job_id):
    # Enforce strict recruiter authorization check
    job = Job.query.filter_by(id=job_id, recruiter_id=current_user.id).first_or_404()

    if request.method == 'POST':
        job.title = request.form.get('title', '').strip()
        job.company = current_user.company_name or request.form.get('company', '').strip() or job.company
        job.location = request.form.get('location', '').strip()
        job.employment_type = request.form.get('employment_type', 'Full-Time')
        job.salary = request.form.get('salary', '').strip()
        job.experience = request.form.get('experience', '').strip()
        job.skills = request.form.get('skills', '').strip()
        job.description = request.form.get('description', '').strip()
        job.openings = request.form.get('openings', job.openings, type=int)
        if 'is_active' in request.form:
            job.is_active = request.form.get('is_active') == 'true'
        
        last_date_str = request.form.get('last_date', '')
        if last_date_str:
            try:
                job.last_date = datetime.strptime(last_date_str, '%Y-%m-%d').date()
            except ValueError:
                flash('Invalid date format.', 'danger')
                return render_template('recruiter/edit_job.html', job=job)

        db.session.commit()
        flash('Job details updated successfully.', 'success')
        return redirect(url_for('main.manage_jobs'))

    return render_template('recruiter/edit_job.html', job=job)

@main.route('/recruiter/delete-job/<int:job_id>', methods=['POST'])
@recruiter_required
def delete_job(job_id):
    # Enforce strict recruiter authorization check
    job = Job.query.filter_by(id=job_id, recruiter_id=current_user.id).first_or_404()

    db.session.delete(job)
    db.session.commit()
    flash('Job posting deleted successfully.', 'success')
    return redirect(url_for('main.manage_jobs'))

@main.route('/recruiter/applications')
@recruiter_required
def view_applications():
    recruiter_jobs = Job.query.filter_by(recruiter_id=current_user.id).all()
    job_ids = [j.id for j in recruiter_jobs]

    job_id_filter = request.args.get('job_id', type=int)
    status_filter = request.args.get('status', '').strip()

    query = Application.query.filter(Application.job_id.in_(job_ids)) if job_ids else Application.query.filter(False)

    if job_id_filter:
        query = query.filter(Application.job_id == job_id_filter)
    if status_filter:
        query = query.filter(Application.status == status_filter)

    applications = query.order_by(Application.applied_date.desc()).all()

    return render_template('recruiter/view_applications.html',
                           applications=applications,
                           recruiter_jobs=recruiter_jobs,
                           selected_job_id=job_id_filter,
                           selected_status=status_filter)

@main.route('/recruiter/applications/<int:app_id>/status', methods=['POST'])
@recruiter_required
def update_application_status(app_id):
    app_item = Application.query.get_or_404(app_id)
    if app_item.job.recruiter_id != current_user.id:
        flash('Unauthorized action.', 'danger')
        return redirect(url_for('main.view_applications'))

    new_status = request.form.get('status', '').strip()
    valid_statuses = ['Applied', 'Under Review', 'Shortlisted', 'Interview', 'Selected', 'Rejected', 'Pending']

    if new_status not in valid_statuses:
        flash('Invalid status provided.', 'danger')
        return redirect(url_for('main.view_applications', job_id=request.args.get('job_id')))

    if new_status == 'Rejected':
        rejection_reason = request.form.get('rejection_reason', '').strip()
        if not rejection_reason:
            flash('Rejection reason is required.', 'danger')
            return redirect(url_for('main.view_applications', job_id=request.args.get('job_id')))
        app_item.rejection_reason = rejection_reason
    else:
        app_item.rejection_reason = None

    app_item.status = new_status
    app_item.updated_at = datetime.utcnow()
    db.session.commit()

    flash(f'Application status updated to "{new_status}" for {app_item.candidate.full_name}.', 'success')
    return redirect(url_for('main.view_applications', job_id=request.args.get('job_id')))

@main.route('/recruiter/profile', methods=['GET', 'POST'])
@recruiter_required
def recruiter_profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', '').strip()
        current_user.company_name = request.form.get('company_name', '').strip()
        current_user.company_description = request.form.get('company_description', '').strip()
        current_user.company_location = request.form.get('company_location', '').strip()
        current_user.company_website = request.form.get('company_website', '').strip()
        current_user.phone = request.form.get('phone', '').strip()
        current_user.address = request.form.get('address', '').strip()
        
        new_password = request.form.get('new_password', '')
        if new_password:
            if len(new_password) < 6:
                flash('New password must be at least 6 characters long.', 'warning')
                return render_template('recruiter/profile.html')
            current_user.set_password(new_password)

        db.session.commit()
        flash('Recruiter profile updated successfully.', 'success')
        return redirect(url_for('main.recruiter_profile'))

    return render_template('recruiter/profile.html')


# -------------------------------------------------------------------
# CANDIDATE MODULE ROUTES
# -------------------------------------------------------------------

@main.route('/candidate/dashboard')
@candidate_required
def candidate_dashboard():
    total_available_jobs = Job.query.filter_by(is_active=True).count()
    my_applications = Application.query.filter_by(candidate_id=current_user.id).all()
    
    total_applied = len(my_applications)
    shortlisted_count = sum(1 for a in my_applications if a.status in ['Shortlisted', 'Interview'])
    selected_count = sum(1 for a in my_applications if a.status == 'Selected')
    
    profile_fields = [current_user.full_name, current_user.email, current_user.phone, 
                      current_user.address, current_user.skills, current_user.education, 
                      current_user.experience, current_user.resume_path]
    completed_fields = sum(1 for field in profile_fields if field)
    profile_completion = int((completed_fields / len(profile_fields)) * 100)

    recent_jobs = Job.query.filter_by(is_active=True).order_by(Job.created_at.desc()).limit(4).all()
    
    return render_template('candidate/dashboard.html',
                           total_available_jobs=total_available_jobs,
                           total_applied=total_applied,
                           shortlisted_count=shortlisted_count,
                           selected_count=selected_count,
                           profile_completion=profile_completion,
                           recent_jobs=recent_jobs)

@main.route('/candidate/browse-jobs')
@candidate_required
def browse_jobs():
    search_query = request.args.get('q', '').strip()
    location_filter = request.args.get('location', '').strip()
    job_type_filter = request.args.get('type', '').strip()
    company_filter = request.args.get('company', '').strip()
    experience_filter = request.args.get('experience', '').strip()

    # Filter only active jobs for candidates
    query = Job.query.filter_by(is_active=True)

    if search_query:
        query = query.filter(
            (Job.title.ilike(f'%{search_query}%')) |
            (Job.company.ilike(f'%{search_query}%')) |
            (Job.skills.ilike(f'%{search_query}%')) |
            (Job.description.ilike(f'%{search_query}%'))
        )

    if location_filter:
        query = query.filter(Job.location.ilike(f'%{location_filter}%'))
    if job_type_filter:
        query = query.filter(Job.employment_type == job_type_filter)
    if company_filter:
        query = query.filter(Job.company.ilike(f'%{company_filter}%'))
    if experience_filter:
        query = query.filter(Job.experience.ilike(f'%{experience_filter}%'))

    jobs = query.order_by(Job.created_at.desc()).all()
    applied_job_ids = [app.job_id for app in Application.query.filter_by(candidate_id=current_user.id).all()]

    locations = db.session.query(Job.location).filter_by(is_active=True).distinct().all()
    companies = db.session.query(Job.company).filter_by(is_active=True).distinct().all()

    return render_template('candidate/browse_jobs.html',
                           jobs=jobs,
                           applied_job_ids=applied_job_ids,
                           search_query=search_query,
                           location_filter=location_filter,
                           job_type_filter=job_type_filter,
                           company_filter=company_filter,
                           experience_filter=experience_filter,
                           locations=[l[0] for l in locations if l[0]],
                           companies=[c[0] for c in companies if c[0]])

@main.route('/candidate/job/<int:job_id>')
@candidate_required
def job_details(job_id):
    job = Job.query.get_or_404(job_id)
    existing_application = Application.query.filter_by(
        candidate_id=current_user.id, 
        job_id=job.id
    ).first()

    return render_template('candidate/job_details.html', 
                           job=job, 
                           existing_application=existing_application)

@main.route('/candidate/apply/<int:job_id>', methods=['GET', 'POST'])
@candidate_required
def apply_job(job_id):
    job = Job.query.get_or_404(job_id)

    if not job.is_active or job.last_date < datetime.utcnow().date():
        flash('This job posting is currently closed or application deadline has passed.', 'danger')
        return redirect(url_for('main.browse_jobs'))

    existing_app = Application.query.filter_by(candidate_id=current_user.id, job_id=job.id).first()

    if existing_app:
        flash('You have already applied for this job.', 'warning')
        return redirect(url_for('main.my_applications'))

    if request.method == 'POST':
        resume_file = request.files.get('resume')
        filename_saved = None

        use_profile_resume = request.form.get('use_profile_resume') == 'true'

        if use_profile_resume and current_user.resume_path:
            filename_saved = current_user.resume_path
        elif resume_file and resume_file.filename:
            if not allowed_file(resume_file.filename):
                flash('Invalid file format. Allowed formats: PDF, DOC, DOCX (Max 10MB).', 'danger')
                return render_template('candidate/apply_job.html', job=job)

            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            original_filename = secure_filename(resume_file.filename)
            timestamp = int(time.time())
            filename_saved = f"candidate_{current_user.id}_{timestamp}_{original_filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename_saved)
            resume_file.save(filepath)

            current_user.resume_path = filename_saved
            db.session.commit()
        else:
            flash('Please upload a resume (PDF/DOC/DOCX) to submit your application.', 'warning')
            return render_template('candidate/apply_job.html', job=job)

        application = Application(
            candidate_id=current_user.id,
            job_id=job.id,
            resume=filename_saved,
            status='Applied'
        )

        db.session.add(application)
        db.session.commit()

        flash('Your job application has been submitted successfully!', 'success')
        return redirect(url_for('main.my_applications'))

    return render_template('candidate/apply_job.html', job=job)

@main.route('/candidate/my-applications')
@candidate_required
def my_applications():
    applications = Application.query.filter_by(candidate_id=current_user.id)\
                                   .order_by(Application.applied_date.desc()).all()
    return render_template('candidate/my_applications.html', applications=applications)

@main.route('/candidate/profile', methods=['GET', 'POST'])
@candidate_required
def candidate_profile():
    if request.method == 'POST':
        current_user.full_name = request.form.get('full_name', '').strip()
        current_user.phone = request.form.get('phone', '').strip()
        current_user.address = request.form.get('address', '').strip()
        current_user.skills = request.form.get('skills', '').strip()
        current_user.education = request.form.get('education', '').strip()
        current_user.experience = request.form.get('experience', '').strip()

        new_password = request.form.get('new_password', '')
        if new_password:
            if len(new_password) < 6:
                flash('Password must be at least 6 characters long.', 'warning')
                return render_template('candidate/profile.html')
            current_user.set_password(new_password)

        resume_file = request.files.get('resume')
        if resume_file and resume_file.filename:
            if not allowed_file(resume_file.filename):
                flash('Invalid file format. Allowed formats: PDF, DOC, DOCX.', 'danger')
                return render_template('candidate/profile.html')

            os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
            original_filename = secure_filename(resume_file.filename)
            timestamp = int(time.time())
            filename_saved = f"profile_{current_user.id}_{timestamp}_{original_filename}"
            filepath = os.path.join(current_app.config['UPLOAD_FOLDER'], filename_saved)
            resume_file.save(filepath)
            
            current_user.resume_path = filename_saved

        db.session.commit()
        flash('Profile updated successfully.', 'success')
        return redirect(url_for('main.candidate_profile'))

    return render_template('candidate/profile.html')


# -------------------------------------------------------------------
# RESUME FILE SERVING ROUTE
# -------------------------------------------------------------------

@main.route('/uploads/resumes/<filename>')
@login_required
def download_resume(filename):
    # Verify user permission (must be recruiter or owner candidate)
    folder = current_app.config['UPLOAD_FOLDER']
    file_path = os.path.join(folder, filename)
    
    if not os.path.exists(file_path):
        flash('Requested resume file not found.', 'danger')
        return redirect(url_for('main.dashboard_redirect'))
        
    return send_from_directory(folder, filename, as_attachment=False)
