<?php
function translate_error($error_msg) {
    $known_errors = [
        // --- Authentification ---
        "Identifiants invalides" => "Adresse email ou mot de passe incorrect.",

        // --- Réinitialisation ---
        "Email non trouvé" => "Aucun compte ne correspond à cet email.",
        "Champs invalides" => "Veuillez remplir tous les champs correctement.",

        // --- Enregistrement utilisateur ---
        "Champs requis manquants ou vides" => "Veuillez remplir tous les champs obligatoires.",
        "Email invalide" => "L'adresse email est invalide.",
        "Mot de passe trop court" => "Le mot de passe doit contenir au moins 6 caractères.",
        "Email déjà utilisé" => "Cette adresse email est déjà associée à un compte.",

        // --- Mise à jour profil ---
        "Accès interdit" => "Vous n'êtes pas autorisé à modifier ce compte.",

        // --- Historique / Photos ---
        "Non autorisé" => "Veuillez vous connecter pour accéder à cette ressource.",
        "Accès interdit à cette photo" => "Vous n’avez pas accès à cette photo.",

        // --- Prédiction IA ---
        "Aucun fichier envoyé" => "Veuillez ajouter une image pour lancer l’identification.",
        "Nom de fichier vide" => "Le nom du fichier est vide. Réessayez avec une autre image.",
        "Animal non reconnu" => "L’animal n’a pas pu être identifié.",

    ];

    return $known_errors[$error_msg] ?? "Une erreur est survenue. Veuillez réessayer plus tard.";
}

?>
