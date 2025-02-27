INSERT INTO Animal (espece, description, nom_latin, famille, taille, region, habitat, fun_fact) VALUES
('Pangolin', 'Le pangolin est un mammifère recouvert d’écailles, vivant principalement en Afrique et en Asie. Il se nourrit de fourmis et de termites.', 'Pholidota', 'Mammifère', '30 à 100 cm', 'Afrique, Asie', 'Forêts tropicales, savanes', 'Le pangolin est le seul mammifère au monde à être entièrement recouvert d’écailles.'),
('Tatou', 'Le tatou est un petit mammifère cuirassé connu pour sa capacité à se rouler en boule pour se protéger des prédateurs.', 'Dasypodidae', 'Mammifère', '15 à 150 cm', 'Amérique du Sud, Amérique centrale', 'Plaines, forêts, zones désertiques', 'Le tatou à neuf bandes peut retenir son souffle jusqu’à six minutes pour traverser les rivières en marchant sous l’eau.'),
('Capybara', 'Le capybara est le plus grand rongeur du monde, vivant principalement en Amérique du Sud, souvent près des cours d’eau.', 'Hydrochoerus hydrochaeris', 'Mammifère', '1 à 1,35 m', 'Amérique du Sud', 'Zones humides, marécages, berges des rivières', 'Le capybara est un excellent nageur et peut rester plusieurs minutes sous l’eau pour échapper à ses prédateurs.'),
('Ornithorynque', 'L’ornithorynque est un mammifère semi-aquatique étonnant qui pond des œufs et possède un bec semblable à celui d’un canard.', 'Ornithorhynchus anatinus', 'Mammifère', '40 à 50 cm', 'Australie', 'Rivières, lacs', 'L’ornithorynque est l’un des rares mammifères venimeux : les mâles possèdent un aiguillon sur leurs pattes arrière.'),
('Tarsier', 'Petit primate nocturne aux grands yeux, le tarsier est un excellent grimpeur qui vit dans les forêts tropicales d’Asie du Sud-Est.', 'Tarsius', 'Mammifère', '10 à 15 cm sans la queue', 'Asie du Sud-Est', 'Forêts tropicales', 'Le tarsier peut tourner sa tête à 180 degrés pour observer son environnement.'),
('Okapi', 'L’okapi est un mammifère africain proche de la girafe, avec un corps sombre et des pattes rayées ressemblant à celles d’un zèbre.', 'Okapia johnstoni', 'Mammifère', '2 à 2,5 m', 'République Démocratique du Congo', 'Forêts denses', 'L’okapi est l’un des rares mammifères capables de lécher ses propres oreilles grâce à sa longue langue.'),
('Dugong', 'Le dugong est un mammifère marin herbivore, souvent confondu avec le lamantin, qui vit dans les eaux côtières chaudes.', 'Dugong dugon', 'Mammifère', '2,5 à 4 m', 'Océan Indien, Pacifique', 'Eaux côtières peu profondes', 'Le dugong est à l’origine du mythe des sirènes en raison de son apparence et de ses comportements aquatiques.');


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