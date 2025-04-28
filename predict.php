<?php
    // Dossier de destination pour l'upload de l'image
    $uploadDir = 'user_data/';
    // Nom du fichier
    $fileName = basename($_FILES['file']['name']);
    
    // Chemin complet du fichier
    $uploadFile = $uploadDir . $fileName;

    // Vérifie si le dossier existe, sinon le créer
    if (!is_dir($uploadDir)) {
        mkdir($uploadDir, 0777, true);
    }

    // Déplacement du fichier temporaire vers le dossier user_data
    if (move_uploaded_file($_FILES['file']['tmp_name'], $uploadFile)) {
        $path = $uploadFile;
    } else {
        echo "Erreur lors de l'upload.";
        exit;
    }

    // URL de l'API Flask
    $url = "http://127.0.0.1:5000/model/predict";

    // Crée un objet CURLFile pour envoyer le fichier image
    $cfile = new CURLFile($path, mime_content_type($path), $fileName);
    
    // Configuration de la requête CURL pour envoyer le fichier image
    $data = array(
        'file' => $cfile
    );

    // Initialiser la session CURL
    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_POST, true);
    curl_setopt($ch, CURLOPT_POSTFIELDS, $data);

    // Exécuter la requête et obtenir la réponse de l'API
    $result = curl_exec($ch);

    if (curl_errno($ch)) {
        echo "Erreur CURL : " . curl_error($ch);
        exit;
    }

    // Fermer la session CURL
    curl_close($ch);

    // Vérifier si la réponse est valide
    if ($result === FALSE) {
        echo "Erreur lors de la connexion à l'API Flask.";
    } else {
        // Décoder la réponse JSON de l'API Flask
        $result = json_decode($result);

        // Si la réponse contient des informations sur l'animal
        if ($result) {
            ?>
            <head>
                <link rel="stylesheet" href="assets/CSS/predict.css"> 
            </head>
            <body>
                <div class="container">
                    <h1>Résultat de la Prédiction</h1>
                    <div class="info"><strong>Description :</strong> <?php echo htmlspecialchars($result->description); ?></div>
                    <div class="info"><strong>Espèce :</strong> <?php echo htmlspecialchars($result->espece); ?></div>
                    <div class="info"><strong>Famille :</strong> <?php echo htmlspecialchars($result->famille); ?></div>
                    <div class="info"><strong>Fait amusant :</strong> <?php echo htmlspecialchars($result->fun_fact); ?></div>
                    <div class="info"><strong>Habitat :</strong> <?php echo htmlspecialchars($result->habitat); ?></div>
                    <div class="info"><strong>Nom latin :</strong> <?php echo htmlspecialchars($result->nom_latin); ?></div>
                    <div class="info"><strong>Région :</strong> <?php echo htmlspecialchars($result->region); ?></div>
                    <div class="info"><strong>Taille :</strong> <?php echo htmlspecialchars($result->taille); ?></div>
                </div>
            </body>
            </html>
            <?php
        } else {
            echo "Aucune information disponible.";
        }
    }
?>
