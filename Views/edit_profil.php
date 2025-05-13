<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}

function handle_api_put_request($url, $data, $token = null) {
    $headers = ['Content-Type: application/json'];
    if ($token) {
        $headers[] = 'Authorization: Bearer ' . $token;
    }

    $ch = curl_init($url);
    curl_setopt($ch, CURLOPT_CUSTOMREQUEST, "PUT");
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, $headers);

    $response = curl_exec($ch);
    if (curl_errno($ch)) {
        return ["error" => "Erreur cURL : " . curl_error($ch)];
    }

    $http_code = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    curl_close($ch);

    if ($http_code >= 400) {
        return ["error" => "Erreur HTTP $http_code"];
    }

    return json_decode($response, true);
}


// Traitement du formulaire
if ($_SERVER['REQUEST_METHOD'] === 'POST' && ($_POST['form_type'] ?? '') === 'update_user') {
    $user_id = $_SESSION['user_id'] ?? null;
    $email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
    $username = trim($_POST['username'] ?? '');

    if (!$user_id || !$email || !$username) {
        $error = "Champs requis manquants.";
    } else {
        $url = "http://127.0.0.1:5000/users/$user_id";
        $data = [
            "email" => $email,
            "username" => $username
        ];

$response = handle_api_put_request($url, $data, $_SESSION['access_token'] ?? null);

        if (isset($response['message']) && $response['message'] === "Utilisateur mis à jour") {
            $_SESSION['user_email'] = $email;
            $_SESSION['user_username'] = $username;
            header("Location: ?page=profil&success=1");
            exit;
        } else {
            $error = htmlspecialchars($response['error'] ?? "Erreur lors de la mise à jour.");
        }
    }
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Modifier mon profil - Wildlens</title>
    <link rel="stylesheet" href="assets/CSS/profil.css">
</head>
<body>
<main class="profil-container" role="main">
    <header>
        <h1>Modifier mon profil</h1>
    </header>
    <?php if (!empty($error)): ?>
            <div style="color:red; background-color: white; padding: 1rem; border-radius: 8px;">
                <?= $error ?>
            </div>
        <?php endif; ?>

    <section class="profil-details" aria-labelledby="edit-profil-info">
        <h2 id="edit-profil-info">Mes informations</h2>

        <form method="post">
            <input type="hidden" name="form_type" value="update_user">

            <div>
                <label for="username">Pseudo :</label><br>
                <input type="text" id="username" name="username" value="<?= htmlspecialchars($_SESSION['user_username'] ?? '') ?>" required>
            </div>

            <div>
                <label for="email">Email :</label><br>
                <input type="email" id="email" name="email" value="<?= htmlspecialchars($_SESSION['user_email'] ?? '') ?>" required>
            </div>

            <br>
            <div class="profil-edit-btn">
                <button type="submit">Valider les modifications</button>
                <a href="?page=profil"><button type="button">Annuler</button></a>
            </div>
        </form>
    </section>
</main>
</body>
</html>
