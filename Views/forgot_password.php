<?php
function handle_api_response($url, $data) {
    $options = [
        'http' => [
            'header'  => "Content-type: application/json\r\n",
            'method'  => 'POST',
            'content' => json_encode($data),
        ]
    ];
    $ctx = stream_context_create($options);
    $response = @file_get_contents($url, false, $ctx);
    if ($response === FALSE) {
        return ["error" => "Impossible de contacter l'API."];
    }
    return json_decode($response, true);
}
?>
<?php
        if ($_SERVER['REQUEST_METHOD'] === 'POST') {
            $url = "http://127.0.0.1:5000/reset-password-direct";
            $email = $_POST['email'] ?? '';
            $password = $_POST['password'] ?? '';

            $data = ['email' => $email, 'password' => $password];
            $response = handle_api_response($url, $data);

            if (isset($response['message'])) {
                echo "<div role='alert' style='color:green;'>{$response['message']}</div>";
            } else {
                echo "<div role='alert' style='color:red;'>{$response['error']}</div>";
            }
        }
        ?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Réinitialiser mon mot de passe</title>
    <link rel="stylesheet" href="assets/CSS/profil.css"> 
</head>
<body>
<main class="profil-container" role="main">
    <header>
        <h1>Réinitialisation de mot de passe</h1>
    </header>

    <section class="profil-details" aria-labelledby="reset-password-info">
        <h2 id="reset-password-info">Veuillez saisir vos informations</h2>

        <form method="post" aria-describedby="reset-password-info">
            <fieldset>
                <legend class="sr-only">Réinitialiser le mot de passe</legend>

                <div class="form-group">
                    <label for="email">Adresse email :</label>
                    <input type="email" id="email" name="email" required>
                </div>

                <div class="form-group">
                    <label for="password">Nouveau mot de passe :</label>
                    <input type="password" id="password" name="password" required>
                </div>

                <div class="form-actions">
                    <button type="submit">Réinitialiser</button>
                    <a href="?page=log">Retour à la connexion</a>
                </div>
            </fieldset>
        </form>
    </section>
</main>
</body>
</html>
