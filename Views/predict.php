<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

if ($_SERVER['REQUEST_METHOD'] === 'POST' && isset($_FILES['file'])) {
    $file = $_FILES['file'];

    if (!is_dir("uploads")) {
        mkdir("uploads", 0777, true);
    }

    if ($file['error'] === UPLOAD_ERR_OK) {
        $upload_path = "uploads/" . basename($file['name']);
        move_uploaded_file($file['tmp_name'], $upload_path);

        $ch = curl_init();
        $cfile = new CURLFile($upload_path, $file['type'], $file['name']);

        curl_setopt_array($ch, [
            CURLOPT_URL => "http://127.0.0.1:5000/model/predict",
            CURLOPT_RETURNTRANSFER => true,
            CURLOPT_POST => true,
            CURLOPT_POSTFIELDS => ['file' => $cfile]
        ]);

        $response = curl_exec($ch);
        $error = curl_error($ch);
        curl_close($ch);
    }
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Résultat de la prédiction</title>
    <link rel="stylesheet" href="assets/CSS/predict.css">
</head>
<body>
<main role="main" class="prediction-container">
    <section aria-labelledby="prediction-title">
        <h1 id="prediction-title">Résultat de la Prédiction</h1>

        <article class="prediction-result">
            <?php
            if (!isset($response)) {
                echo "<p role='alert' class='error'> Aucune image reçue.</p>";
            } elseif ($error) {
                echo "<p role='alert' class='error'>Erreur cURL : " . htmlspecialchars($error) . "</p>";
            } else {
                $data = json_decode($response);

                if (isset($data->message)) {
                    echo "<p role='alert' class='error'>" . htmlspecialchars($data->message) . "</p>";
                } elseif (isset($data->error)) {
                    echo "<p role='alert' class='error'>Erreur serveur : " . htmlspecialchars($data->error) . "</p>";
                } else {
                    function safeEcho($label, $value) {
                        if (!empty($value)) {
                            echo "<p><strong>$label</strong> : " . htmlspecialchars($value) . "</p>";
                        }
                    }

                   echo "<section class='prediction-details'>";

// Image de l'espèce prédite
if (!empty($data->espece)) {
    $imagePath = "assets/images/" . htmlspecialchars($data->espece) . ".png";
    echo "<img src='$imagePath' alt='Photo de " . htmlspecialchars($data->espece) . "' class='animal'>";
}

// Les infos textuelles
safeEcho("Description", $data->description ?? null);
safeEcho("Espèce", $data->espece ?? null);
safeEcho("Famille", $data->famille ?? null);
safeEcho("Fait amusant", $data->fun_fact ?? null);
safeEcho("Habitat", $data->habitat ?? null);
safeEcho("Nom latin", $data->nom_latin ?? null);
safeEcho("Région", $data->region ?? null);
safeEcho("Taille", $data->taille ?? null);

echo "</section>";


                    // Enregistrement si connecté
                    if (isset($_SESSION['user_id']) && isset($data->espece)) {
                        try {
                            $db = new PDO("mysql:host=localhost;dbname=wildlens", "root", "");
                            $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

                            $stmt = $db->prepare("SELECT id FROM animal WHERE espece = ?");
                            $stmt->execute([$data->espece]);
                            $animal = $stmt->fetch();
                            $animal_id = $animal ? $animal['id'] : null;

                            $stmt = $db->prepare("INSERT INTO photo (file_name, animal_id, user_id) VALUES (?, ?, ?)");
                            $stmt->execute([$file['name'], $animal_id, $_SESSION['user_id']]);
                            $photo_id = $db->lastInsertId();

                            $location_id = isset($_POST['city_id']) ? (int)$_POST['city_id'] : 1;

                            $stmt = $db->prepare("INSERT INTO scanhistory (photo_id, user_id, location_id) VALUES (?, ?, ?)");
                            $stmt->execute([$photo_id, $_SESSION['user_id'], $location_id]);

                        } catch (PDOException $e) {
                            echo "<p class='error'>Erreur base de données : " . htmlspecialchars($e->getMessage()) . "</p>";
                        }
                    }
                }
            }
            ?>
        </article>
    </section>
</main>
</body>
</html>
