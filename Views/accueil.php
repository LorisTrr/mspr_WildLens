<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Accueil - Wildlens</title>
    <link rel="stylesheet" href="assets/CSS/accueil.css">
</head>
<body>
    <main class="scan-container">
        <h1>Scannez une trace de pas !</h1>
        <div class="scan-section">
        <p class="intro-text">
            A partir de notre site web, vous pouvez importer une photo depuis votre ordinateur
        </p>
            <div class="scan-image">
                <img src="assets/images/phone.png" alt="Illustration empreinte sur téléphone">
            </div>
            

            <form class="scan-form" action="?page=predict" method="POST" enctype="multipart/form-data">
                <label for="file">Choisissez votre photo :</label>
                <input type="file" name="file" id="file" accept="image/*" required>

                <label for="city">Ville la plus proche :</label>
                <select name="city_id" id="city" required>
                    <option value="">Choisissez la ville la plus proche</option>
                    <?php
                    try {
                        $db = new PDO("mysql:host=localhost;dbname=wildlens", "root", "");
                        $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

                        $stmt = $db->query("SELECT id, city FROM location ORDER BY city ASC");
                        while ($row = $stmt->fetch()) {
                            echo "<option value='" . htmlspecialchars($row['id']) . "'>" . htmlspecialchars($row['city']) . "</option>";
                        }
                    } catch (PDOException $e) {
                        echo "<option disabled>Erreur : " . htmlspecialchars($e->getMessage()) . "</option>";
                    }
                    ?>
                </select>

                <button type="submit">Envoyer</button>
            </form>
        </div>
    </main>
</body>
</html>
