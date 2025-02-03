
-- Création de la base de données
CREATE DATABASE IF NOT EXISTS wild_lens;
USE animaux_quebec;

-- Suppression des tables si elles existent déjà
DROP TABLE IF EXISTS animal;
DROP TABLE IF EXISTS categorie_animal;

-- Création des tables
CREATE TABLE categorie_animal (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50) NOT NULL
);

CREATE TABLE animal (
    id INT PRIMARY KEY AUTO_INCREMENT,
    nom VARCHAR(50) NOT NULL,
    description TEXT,
    lieu VARCHAR(100),
    categorie_id INT,
    FOREIGN KEY (categorie_id) REFERENCES categorie_animal(id)
);

-- Insertion des catégories
INSERT INTO categorie_animal (nom) VALUES
('Mammifère');

-- Insertion des animaux
INSERT INTO animal (nom, description, lieu, categorie_id) VALUES
('Castor', 'Rongeur semi-aquatique connu pour construire des barrages', 'Cours d''eau et lacs', 1),
('Chien', 'Animal domestique fidèle et affectueux', 'Habitat humain', 1),
('Chat', 'Félin domestique indépendant', 'Habitat humain', 1),
('Coyote', 'Canidé sauvage adaptable', 'Forêts et prairies', 1),
('Écureuil', 'Petit rongeur arboricole', 'Forêts', 1),
('Lapin', 'Petit mammifère aux longues oreilles', 'Prairies et forêts', 1),
('Loup', 'Canidé sauvage social', 'Forêts', 1),
('Lynx', 'Félin sauvage aux oreilles pointues', 'Forêts', 1),
('Ours', 'Grand mammifère omnivore', 'Forêts', 1),
('Puma', 'Grand félin aussi appelé cougar', 'Montagnes et forêts', 1),
('Raton laveur', 'Mammifère nocturne aux pattes agiles', 'Forêts et zones urbaines', 1),
('Renard', 'Canidé rusé et adaptable', 'Forêts et zones urbaines', 1);

