CREATE DATABASE IF NOT EXISTS patient_portal;
USE patient_portal;

-- Users table (common for all user types)
CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(255) NOT NULL UNIQUE,
    name VARCHAR(255) NOT NULL,
    role ENUM('patient', 'clinician', 'admin') NOT NULL,
    google_id VARCHAR(255) UNIQUE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Patient queries
CREATE TABLE queries (
    id INT AUTO_INCREMENT PRIMARY KEY,
    patient_id INT NOT NULL,
    question TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (patient_id) REFERENCES users(id)
);

-- AI and clinician responses
CREATE TABLE responses (
    id INT AUTO_INCREMENT PRIMARY KEY,
    query_id INT NOT NULL,
    ai_response TEXT NOT NULL,
    clinician_response TEXT,
    clinician_id INT,
    status ENUM('unreviewed', 'reviewed', 'edited') DEFAULT 'unreviewed',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    reviewed_at TIMESTAMP,
    FOREIGN KEY (query_id) REFERENCES queries(id),
    FOREIGN KEY (clinician_id) REFERENCES users(id)
);