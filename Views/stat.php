<!DOCTYPE html>
<head>
    <link rel="stylesheet" href="CSS/stat.css">
</head>
<body>
<div class="stats-container">
    <h1 class="stats-title">Statistiques TrackFinder</h1>

    <div class="cards-grid">
        <div class="stat-card">
            <h3>Scans totaux</h3>
            <div class="stat-number">3,847</div>
            <div class="stat-trend">+156 cette semaine</div>
        </div>

        <div class="stat-card">
            <h3>Espèces identifiées</h3>
            <div class="stat-number">42</div>
            <div class="stat-trend">Dans notre base de données</div>
        </div>

        <div class="stat-card">
            <h3>Utilisateurs actifs</h3>
            <div class="stat-number">892</div>
            <div class="stat-trend">Ce mois-ci</div>
        </div>
    </div>

    <div class="charts-grid">
        <div class="chart-container">
            <h3>Top 5 des espèces identifiées</h3>
            <canvas id="speciesChart"></canvas>
        </div>

        <div class="chart-container">
            <h3>Scans mensuels</h3>
            <canvas id="activityChart"></canvas>
        </div>
    </div>
</div>

<script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
<script>
    // Graphique des espèces les plus identifiées
    const speciesCtx = document.getElementById('speciesChart').getContext('2d');
    new Chart(speciesCtx, {
        type: 'bar',
        data: {
            labels: ['Cerf', 'Sanglier', 'Renard', 'Chevreuil', 'Lièvre'],
            datasets: [{
                label: 'Nombre de scans',
                data: [856, 645, 489, 423, 312],
                backgroundColor: [
                    '#2ecc71',
                    '#3498db',
                    '#e74c3c',
                    '#f1c40f',
                    '#9b59b6'
                ]
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });

    // Graphique d'activité mensuelle
    const activityCtx = document.getElementById('activityChart').getContext('2d');
    new Chart(activityCtx, {
        type: 'line',
        data: {
            labels: ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Juin'],
            datasets: [{
                label: 'Nombre de scans',
                data: [250, 320, 450, 580, 670, 856],
                borderColor: '#2ecc71',
                tension: 0.3,
                fill: false
            }]
        },
        options: {
            responsive: true,
            scales: {
                y: {
                    beginAtZero: true
                }
            }
        }
    });
</script>
