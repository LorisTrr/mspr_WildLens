<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
<!DOCTYPE html>
<html data-theme="dark" lang="fr">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Wildlense - Accueil</title>
    <!-- Lien vers un fichier CSS externe -->
    <link rel="stylesheet" href="assets/CSS/variable.css">
    <link rel="stylesheet" href="assets/CSS/header.css">
    <link rel="shortcut icon" type="image/png" href="assets/images/favicon.png"/>
</head>
<body>
<main>
    <section>
    <div class="header">
        <div class="logo-menu-icon">
            <img src="assets/images/logo_white.png" class='logo' alt="logo du site">
            <button class="menu-toggle" id="menu-toggle">
                &#9776; <!-- icône hamburger -->
            </button>
        </div>
        <nav class="nav" id="nav">
            <ul>
            <li><a href="?page=accueil">Accueil</a></li>
            <li><a href="?page=animale">Catégorie Animale</a></li>
            <li><a href="?page=findanimals">Où trouver quel animal ? </a></li>
            <li><a href="?page=stat">Statistique</a></li>
            <li>
            <?php if (isset($_SESSION['is_logged_in']) && $_SESSION['is_logged_in']) { ?>
            <li><a href="?page=historique">Historique</a></li>
            <li><a href="?page=profil">Mon Profil</a></li>
            <li><a href="?page=logout">Se déconnecter</a></li>
        <?php } else { ?>
            <li><a href="?page=log">Se connecter</a></li>
        <?php } ?>
            </ul>
        </nav>

        <svg class="icon-theme" viewBox="0 0 507.884 507.765" xmlns="http://www.w3.org/2000/svg">
            <path d="M216.043 510.47c-34.074-5.712-73.642-22.116-102.04-42.303-19.721-14.02-47.384-41.424-61.24-60.669-31.046-43.118-46.99-93.276-46.99-147.816 0-70.643 25.963-132.079 76.69-181.462 21.62-21.046 38.418-33.29 62.609-45.636 81.985-41.838 185.41-34.521 260.4 18.423 18.53 13.082 47.798 42.092 61.089 60.552 21.877 30.384 37.7 68.108 44.198 105.367 3.863 22.154 3.863 63.358 0 85.512-18.58 106.544-103.665 191.065-209.644 208.253-22.497 3.649-62.611 3.545-85.072-.22zm87.365-90.804c18.607-4.46 41.183-14.254 55.713-24.17 29.469-20.107 57.669-56.999 66.739-87.308 2.266-7.572 2.148-8.93-1.083-12.5-4.626-5.112-11.066-5.076-21.246.117-24.005 12.247-66.505 15.848-96.046 8.139-47.616-12.425-84.258-47.002-100.954-95.262-5.017-14.503-5.537-18.62-5.55-44-.012-25.035.551-29.689 5.32-43.955 4.848-14.497 5.063-16.37 2.357-20.5-3.934-6.003-10.534-5.8-23.452.724-42.88 21.655-74.644 61.403-87.69 109.731-6.325 23.434-6.35 61.663-.054 84.976 9.292 34.409 31.87 69.742 57.758 90.388 21.543 17.181 53.264 32.001 74.538 34.823 8.8 1.168 9.905.84 12.982-3.857 3.785-5.776 2.639-12.33-2.65-15.16-1.876-1.004-9.168-3.317-16.205-5.14-15.554-4.031-32.987-12.575-49.395-24.211-41.113-29.155-65.651-86.179-58.756-136.539 5.118-37.382 16.881-61.24 43.279-87.78 10.12-10.175 19.285-18.5 20.367-18.5 1.288 0 1.286 2.934-.007 8.5-1.086 4.675-1.572 19.75-1.08 33.5.763 21.371 1.82 27.758 7.288 44 18.596 55.247 61.399 95.515 117.191 110.25 20.352 5.374 57.673 5.977 76.988 1.243 7.144-1.75 13.355-2.816 13.804-2.368 1.676 1.677-14.869 24.253-25.107 34.258-13.13 12.833-25.038 21.12-41.226 28.696-15.724 7.357-41.142 13.921-53.91 13.921-11.094 0-16.464 2.236-19.645 8.18-1.691 3.16-1.464 5.194 1 8.954 2.892 4.414 4.53 4.865 17.642 4.852 7.95-.008 21.94-1.809 31.09-4.002z" fill="currentColor"/>
        </svg>
    </div>
    </section>
</main>
</body>