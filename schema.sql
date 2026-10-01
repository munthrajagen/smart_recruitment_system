-- Smart Recruitment System Database Schema (MySQL 8.0+)
-- Create Database
CREATE DATABASE IF NOT EXISTS smart_recruitment_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;

USE smart_recruitment_db;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    full_name VARCHAR(120) NOT NULL,
    email VARCHAR(120) NOT NULL UNIQUE,
    password_hash VARCHAR(256) NOT NULL,
    role VARCHAR(20) NOT NULL,
    company_name VARCHAR(200) NULL,
    company_description TEXT NULL,
    company_location VARCHAR(200) NULL,
    company_website VARCHAR(300) NULL,
    phone VARCHAR(20) NULL,
    address VARCHAR(255) NULL,
    skills TEXT NULL,
    education TEXT NULL,
    experience TEXT NULL,
    resume_path VARCHAR(255) NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    INDEX idx_user_email (email),
    INDEX idx_user_role (role)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 2. Jobs Table
CREATE TABLE IF NOT EXISTS jobs (
    id INT AUTO_INCREMENT PRIMARY KEY,
    recruiter_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    company VARCHAR(150) NOT NULL,
    location VARCHAR(100) NOT NULL,
    employment_type VARCHAR(50) NOT NULL,
    salary VARCHAR(100) NOT NULL,
    experience VARCHAR(50) NOT NULL,
    skills TEXT NOT NULL,
    description TEXT NOT NULL,
    last_date DATE NOT NULL,
    openings INT DEFAULT 1 NOT NULL,
    is_active TINYINT(1) DEFAULT 1 NOT NULL,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (recruiter_id) REFERENCES users(id) ON DELETE CASCADE,
    INDEX idx_job_title (title),
    INDEX idx_job_location (location),
    INDEX idx_job_company (company),
    INDEX idx_job_active (is_active)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- 3. Applications Table
CREATE TABLE IF NOT EXISTS applications (
    id INT AUTO_INCREMENT PRIMARY KEY,
    candidate_id INT NOT NULL,
    job_id INT NOT NULL,
    resume VARCHAR(255) NOT NULL,
    status VARCHAR(30) DEFAULT 'Applied' NOT NULL,
    rejection_reason TEXT NULL,
    applied_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (candidate_id) REFERENCES users(id) ON DELETE CASCADE,
    FOREIGN KEY (job_id) REFERENCES jobs(id) ON DELETE CASCADE,
    UNIQUE KEY unique_candidate_job (candidate_id, job_id),
    INDEX idx_app_status (status)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
