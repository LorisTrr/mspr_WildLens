<head>
    <link rel="stylesheet" href="CSS/log.css">
</head>
<?php
if(isset($_POST['form_type']) && $_POST['form_type'] === 'login'){
    $url = "http://127.0.0.1:5000/login";
    $data = array(
        "email" => $_POST['email'],
        "password" => md5($_POST['password-log'])
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

        if($result->email){
            $_SESSION['user_email'] = $result->email;
            $_SESSION['user_id'] = $result->id;
            echo "Connexion réussie";
        } else {
            echo "Erreur lors de la connexion";
        }
    }
}

if(isset($_POST['register'])){
    $email = $_POST['mail'];
    $password = hash('sha256', $_POST['password']);
    $password2 = hash('sha256', $_POST['password2']);
    if($password === $password2){
        $url = "http://127.0.0.1:5000/users";
        $data = array(
            "username" => $_POST['pseudo'], // Remplacez par le nom d'utilisateur souhaité
            "email" => $email,
            "password" => $password,
            "first_name" => $_POST['nom'], // Remplacez par le prénom souhaité
            "last_name" => $_POST['prenom'] // Remplacez par le nom souhaité
        );

        $options = [
            'http' => array(
                'header'  => "Content-type: application/json\r\n",
                'method'  => 'POST',
                'content' => json_encode($data),
            ),
        ];


        $context  = stream_context_create($options);
        $result = file_get_contents($url, false, $context);

        if ($result === FALSE) {
            echo "Erreur lors de l'ajout de l'utilisateur";
        } else {
            echo "Utilisateur ajouté avec succès";
        }
    } else {
        echo "Les mots de passe ne correspondent pas";
    }
}
    
?>
<body>
    <div class="container-log">
        <div class="log">
            <h1>Connexion</h1>
            <p>Connectez-vous pour accéder à votre compte</p>
            <form method="post" action="?page=log">
                <input name="email" placeholder="Votre e-mail" type='mail' />
                <input type='hidden' value='login' name='form_type' value='login'>
                <input name="password-log" placeholder="Votre mdp" type='password' />
                <button type="submit">Se connecter</button>
            </form>
        </div>
        <div class=register>
            <h1>Inscription</h1>
            <p>Créez un compte pour accéder à toutes les fonctionnalités</p>
            <form method="post" action="?page=log">
            <input type='hidden' name='register' value='register'>

                <input name="nom" placeholder="Nom" type='text' />
                <input name="prenom" placeholder="Prénom" type='text' />
                <input name="pseudo" placeholder="Pseudo" type='text' />
                <input name="mail" placeholder="Votre e-mail" type='mail' />
                <input name="password" placeholder="Votre mdp" type='password' />
                <input name="password2" placeholder="Confirmer votre mdp" type='password' />
                <button type="submit">S'inscrire</button>
            </form>
        </div>
    </div>
</body>