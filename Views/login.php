<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
require_once 'api/log.php';

function handle_api_response($url, $data) {
    $ch = curl_init($url);

    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    curl_setopt($ch, CURLOPT_HTTPHEADER, ["Content-Type: application/json"]);
    curl_setopt($ch, CURLOPT_POSTFIELDS, json_encode($data));
    curl_setopt($ch, CURLOPT_POST, true);

    $response = curl_exec($ch);
    $httpCode = curl_getinfo($ch, CURLINFO_HTTP_CODE);
    $errorCurl = curl_error($ch);

    curl_close($ch);

    if ($response === false) {
        return ["error" => "Erreur de connexion : $errorCurl"];
    }

    $decoded = json_decode($response, true);

    if ($httpCode >= 400) {
        return ["error" => $decoded['error'] ?? "Erreur HTTP $httpCode"];
    }

    return $decoded;
}


$form_type = $_POST['form_type'] ?? '';

if ($form_type === 'login') {
    $email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
    $password = $_POST['password'] ?? '';

    if (!$email || !$password) {
        echo "<div role='alert' style='color:red;'>Veuillez remplir tous les champs.</div>";
    } else {
        $url = "http://127.0.0.1:5000/login";
        $data = ["email" => $email, "password" => $password];

        $response = handle_api_response($url, $data);

        if (isset($response['access_token'])) {
            if (session_status() === PHP_SESSION_NONE) {
                session_start();
            }

            $_SESSION['is_logged_in'] = true;
            $_SESSION['user_email'] = $email;
            $_SESSION['user_username'] = $response['username'] ?? '';
            $_SESSION['user_id'] = $response['id'] ?? null;
            $_SESSION['access_token'] = $response['access_token'];

            header("Location: ?page=profil");
            exit;
        } else {
            $raw = $response['error'] ?? "Connexion échouée.";
            $msg = translate_error($raw);
            echo "<div role='alert' style='color:red;'>$msg</div>";
        }
    }

} elseif ($form_type === 'register') {
    $nom = trim($_POST['nom'] ?? '');
    $prenom = trim($_POST['prenom'] ?? '');
    $pseudo = trim($_POST['pseudo'] ?? '');
    $email = filter_var($_POST['email'] ?? '', FILTER_VALIDATE_EMAIL);
    $password = $_POST['password'] ?? '';
    $confirm = $_POST['confirm_password'] ?? '';

    if (!$nom || !$prenom || !$pseudo || !$email || !$password || $password !== $confirm) {
        echo "<div role='alert' style='color:red;'>Champs invalides ou mots de passe différents.</div>";
    } else {
        $url = "http://127.0.0.1:5000/users";
        $data = [
            "username"   => $pseudo,
            "email"      => $email,
            "password"   => $password,
            "first_name" => $prenom,
            "last_name"  => $nom
        ];

        $response = handle_api_response($url, $data);

        if (isset($response['message']) && $response['message'] === "Utilisateur enregistré") {
            if (session_status() === PHP_SESSION_NONE) {
                session_start();
            }

            $_SESSION['is_logged_in'] = true;
            $_SESSION['user_email'] = $email;
            $_SESSION['user_username'] = $pseudo;
            $_SESSION['user_id'] = $response['id'] ?? null;

            header("Location: ?page=profil");
            exit;
        } else {
            $raw = $response['error'] ?? "Inscription échouée.";
            $msg = translate_error($raw);
            echo "<div role='alert' style='color:red;'>$msg</div>";
        }
    }
}


?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Accueil - Wildlens</title>
    <link rel="stylesheet" href="assets/CSS/log.css">
</head>
<body>
    <main class="scan-container">
         <div class="container">
        <section aria-labelledby="login-title">
           
            <form method="post" aria-describedby="login-desc">
                 <h2 id="login-title">Connexion</h2>
                <input type="hidden" name="form_type" value="login">
                <p id="login-desc">Connectez-vous pour accéder à votre compte.</p>

                <label class='label' for="email">Adresse e-mail :</label>
                <input type="email" id="email" name="email" required>

                <label class='label' for="password">Mot de passe :</label>
                <input type="password" id="password" name="password" required>

                <button type="submit">Se connecter</button>
                <a href="?page=forgot_password">Mot de passe oublié ?</a>

            </form>
        </section>

        <section aria-labelledby="register-title">
          
            <form method="post" aria-describedby="register-desc">
                  <h2 id="register-title">Inscription</h2>
                <input type="hidden" name="form_type" value="register">
                <p id="register-desc">Créez un compte pour accéder à toutes les fonctionnalités.</p>

                <label for="nom">Nom :</label>
                <input type="text" id="nom" name="nom" required>

                <label for="prenom">Prénom :</label>
                <input type="text" id="prenom" name="prenom" required>

                <label for="pseudo">Pseudo :</label>
                <input type="text" id="pseudo" name="pseudo" required>

                <label for="email_reg">Adresse e-mail :</label>
                <input type="email" id="email_reg" name="email" required>

                <label for="password_reg">Mot de passe :</label>
                <input type="password" id="password_reg" name="password" required>

                <label for="confirm_password">Confirmez le mot de passe :</label>
                <input type="password" id="confirm_password" name="confirm_password" required>

                <button type="submit">S'inscrire</button>
            </form>
        </section>
    </div>
    </main>
</body>
</html>
