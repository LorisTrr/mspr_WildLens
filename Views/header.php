<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wildlense - Accueil</title>
    <!-- Lien vers un fichier CSS externe -->
    <link rel="stylesheet" href="CSS/header.css">
    <link rel="shortcut icon" type="image/png" href="assets/images/favicon.png"/>
</head>
<body>
    <div class="nav">
        <img src="assets/images/logo_white.png" alt="logo du site">
        <div class="element-nav">
            <a href="?page=accueil">Accueil</a>
        </div>
        <div class="element-nav">
            <a href="?page=animale">Catégorie Animale</a>
        </div>
        <div class="element-nav">
            <a href="?page=stat">Statistique</a>
        </div>
        <div class="element-nav">
            <a href="?page=findanimals">Où trouver quel animal ? </a>
        </div>
        <div class="element-nav">
            <?php if($is_logged_in) { ?>
                <a href="?page=log">Se déconnecter </a>
                <?php } else { ?>
                     <a href="?page=log">Se connecter </a>
                <?php } ?>
        </div>
    </div>
</body>