<?php

class DatabaseLoader {
    private $pdo;

    public function __construct() {
        try {
            $this->pdo = new PDO(
                'mysql:host=localhost;dbname=wild_lens;charset=utf8',
                'root',
                '',
                [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
            );
        } catch (PDOException $e) {
            die('Erreur de connexion à la base de données : ' . $e->getMessage());
        }
    }

    public function getAllAnimals() {
        $query = "SELECT a.*, c.nom as categorie_nom 
                 FROM animal a
                 JOIN categorie_animal c ON a.categorie_id = c.id";
        $stmt = $this->pdo->query($query);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    public function getAnimalById($id) {
        $query = "SELECT a.*, c.nom as categorie_nom 
                 FROM animal a
                 JOIN categorie_animal c ON a.categorie_id = c.id 
                 WHERE a.id = :id";
        $stmt = $this->pdo->prepare($query);
        $stmt->execute(['id' => $id]);
        return $stmt->fetch(PDO::FETCH_ASSOC);
    }

    public function getAnimalsByCategory($categoryId) {
        $query = "SELECT a.*, c.nom as categorie_nom 
                 FROM animal a
                 JOIN categorie_animal c ON a.categorie_id = c.id 
                 WHERE a.categorie_id = :categoryId";
        $stmt = $this->pdo->prepare($query);
        $stmt->execute(['categoryId' => $categoryId]);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }

    public function getAllCategories() {
        $query = "SELECT * FROM categorie_animal";
        $stmt = $this->pdo->query($query);
        return $stmt->fetchAll(PDO::FETCH_ASSOC);
    }
}
