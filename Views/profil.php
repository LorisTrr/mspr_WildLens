<?php
if (session_status() === PHP_SESSION_NONE) {
    session_start();
}
if (!isset($_SESSION['is_logged_in']) || !$_SESSION['is_logged_in']) {
    header("Location: ?page=log");
    exit;
}
?>

<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Accueil - Wildlens</title>
    <link rel="stylesheet" href="assets/CSS/profil.css">
</head>
<body>
  <main class="profil-container" role="main">
  <header>
    <h1>Bienvenue sur votre profil</h1>
  </header>
<?php if (isset($_GET['success']) && $_GET['success'] == 1): ?>
    <div style="color:green;">Votre profil a bien été mis à jour.</div>
<?php endif; ?>
  <section class="profil-details" aria-labelledby="profil-info">
    <h2 id="profil-info">Informations de votre compte</h2>
    <dl>
      <div>
        <dt><label for="email">Adresse e-mail :</label></dt>
        <dd id="email"><?= htmlspecialchars($_SESSION['user_email']) ?></dd>
      </div>
     <div>
  <dt><label for="pseudo">Pseudo :</label></dt>
  <dd id="pseudo"><?= htmlspecialchars($_SESSION['user_username']) ?></dd>
</div>
    </dl>
  </section>

  <nav class="profil-edit-btn" aria-label="Actions utilisateur">
    <a href="?page=edit_profil" style="display:inline-block; margin-right: 1rem;">
  <button>Modifier mon compte</button>
</a>


    <form action="?page=logout" method="post" style="display:inline-block;">
      <button type="submit">Se déconnecter</button>
    </form>
  </nav>
</main>

</body>
</html>