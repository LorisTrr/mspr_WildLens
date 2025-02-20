
DROP DATABASE IF EXISTS wildlens;
CREATE DATABASE wildlens;

USE wildlens;

-- Create User table
CREATE TABLE User (
    id INT PRIMARY KEY AUTO_INCREMENT,
    username VARCHAR(50) NOT NULL UNIQUE,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL,
    first_name VARCHAR(50),
    last_name VARCHAR(50),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create Animal table
CREATE TABLE Animal (
    id INT PRIMARY KEY AUTO_INCREMENT,
    espece VARCHAR(100) NOT NULL,
    description TEXT,
    nom_latin VARCHAR(100),
    famille VARCHAR(50),
    taille VARCHAR(50),
    region VARCHAR(100),
    habitat TEXT,
    fun_fact TEXT
);

-- Create Location table
CREATE TABLE Location (
    id INT PRIMARY KEY AUTO_INCREMENT,
    country VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    latitude DECIMAL(10, 8),
    longitude DECIMAL(11, 8)
);

-- Create Photo table
CREATE TABLE Photo (
    id INT PRIMARY KEY AUTO_INCREMENT,
    file_path VARCHAR(255) NOT NULL,
    file_name VARCHAR(255) NOT NULL,
    upload_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    animal_id INT,
    FOREIGN KEY (animal_id) REFERENCES Animal(id)
);

-- Create ScanHistory table
CREATE TABLE ScanHistory (
    id INT PRIMARY KEY AUTO_INCREMENT,
    photo_id INT NOT NULL,
    user_id INT NOT NULL,
    location_id INT NOT NULL,
    scan_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (photo_id) REFERENCES Photo(id),
    FOREIGN KEY (user_id) REFERENCES User(id),
    FOREIGN KEY (location_id) REFERENCES Location(id)
);


-- Insert Users
INSERT INTO User (username, email, password, first_name, last_name) VALUES
('jdoe', 'jdoe@example.com', 'hashed_password1', 'John', 'Doe'),
('asmith', 'asmith@example.com', 'hashed_password2', 'Alice', 'Smith'),
('bwayne', 'bwayne@example.com', 'hashed_password3', 'Bruce', 'Wayne'),
('cdupont', 'cdupont@example.com', 'hashed_password4', 'Claire', 'Dupont'),
('pmartin', 'pmartin@example.com', 'hashed_password5', 'Paul', 'Martin'),
('evincent', 'evincent@example.com', 'hashed_password6', 'Emma', 'Vincent');


-- Insert Locations
INSERT INTO Location (country, city, latitude, longitude) VALUES
('France', 'Paris', 48.8566, 2.3522),
('France', 'Marseille', 43.2965, 5.3698),
('France', 'Lyon', 45.7640, 4.8357),
('France', 'Toulouse', 43.6047, 1.4442),
('France', 'Nice', 43.7102, 7.2620),
('France', 'Nantes', 47.2184, -1.5536),
('France', 'Strasbourg', 48.5734, 7.7521),
('France', 'Montpellier', 43.6117, 3.8772),
('France', 'Bordeaux', 44.8378, -0.5792),
('France', 'Lille', 50.6292, 3.0573);

-- Insert Photos
INSERT INTO Photo (file_path, file_name, animal_id) VALUES
('/uploads/tiger1.jpg', 'tiger1.jpg', 1),
('/uploads/eagle1.jpg', 'eagle1.jpg', 2),
('/uploads/dolphin1.jpg', 'dolphin1.jpg', 3),
('/uploads/wolf1.jpg', 'wolf1.jpg', 4),
('/uploads/tiger2.jpg', 'tiger2.jpg', 1),
('/uploads/eagle2.jpg', 'eagle2.jpg', 2);

-- Insert ScanHistory
INSERT INTO ScanHistory (photo_id, user_id, location_id) VALUES
(1, 1, 2),
(2, 2, 3),
(3, 3, 1),
(4, 4, 4),
(5, 5, 5),
(6, 6, 6);