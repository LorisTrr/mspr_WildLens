
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

