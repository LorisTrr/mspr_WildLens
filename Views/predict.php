<?php 
    // Dossier de destination
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
    }
    $url = "http://127.0.0.1:5000/model/predict";
    $data = array(
        "path" => $path,
    );
    $options = array(
        'http' => array(
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data),
        ),
    );
    $context = stream_context_create($options);
    $result = file_get_contents($url, false, $context);
    if ($result === FALSE) {
        echo "Erreur lors de la connexion";
    } else {
        $result = json_decode($result);
        ?>
<head>
    <link rel="stylesheet" href="CSS/predict.css"> 
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
    }
?>

