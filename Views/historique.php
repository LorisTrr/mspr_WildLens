<?php
try {
    $db = new PDO("mysql:host=localhost;dbname=wildlens", "root", "");
    $db->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    $stmt = $db->prepare("
        SELECT h.scan_date, p.file_name, l.city AS lieu_nom, a.espece
        FROM scanhistory h
        JOIN photo p ON h.photo_id = p.id
        JOIN animal a ON p.animal_id = a.id
        JOIN location l ON h.location_id = l.id
        WHERE h.user_id = ?
        ORDER BY h.scan_date DESC
    ");
    $stmt->execute([$_SESSION['user_id']]);
    $scans = $stmt->fetchAll();
}
catch (PDOException $e) {
    echo "<p class='error'>Erreur : " . htmlspecialchars($e->getMessage()) . "</p>";
}
?>
<!DOCTYPE html>
<html lang="fr">
<head>
    <meta charset="UTF-8">
    <title>Historique des scans</title>
    <link rel="stylesheet" href="assets/CSS/historique.css">
</head>
<body>
    <main class="historique-container" role="main">
       <table class="table-historique">
  <caption>Liste des scans effectués par l'utilisateur</caption>
  <thead>
    <tr>
      <th scope="col">Date</th>
      <th scope="col">Image</th>
      <th scope="col">Espèce</th>
      <th scope="col">Lieu</th>
    </tr>
  </thead>
  <tbody>
     <?php if (!empty($scans)): ?>
        <?php foreach ($scans as $scan): ?>
      <tr>
        <td data-label="Date"><?= htmlspecialchars($scan['scan_date']) ?></td>
        <td data-label="Image">
          <img src="uploads/<?= htmlspecialchars($scan['file_name']) ?>" alt="Empreinte de <?= htmlspecialchars($scan['espece']) ?>" width="80">
        </td>
        <td data-label="Espèce"><?= htmlspecialchars($scan['espece']) ?></td>
        <td data-label="Lieu"><?= htmlspecialchars($scan['lieu_nom']) ?></td>
      </tr>
    <?php endforeach; ?>
    <?php else: ?>
        <tr>
            <td colspan="4" style="text-align: center;">Vous n'avez pas encore de scan enregistré.</td>
        </tr>
    <?php endif; ?>
  </tbody>
</table>
    </main>
</body>
</html>
