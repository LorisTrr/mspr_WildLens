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
            <div id="scansTotal" class="stat-number">Chargement...</div>
            <div id="scansTrend" class="stat-trend">Chargement...</div>
        </div>

        <div class="stat-card">
            <h3>Espèces identifiées</h3>
            <div id="speciesIdentified" class="stat-number">Chargement...</div>
            <div class="stat-trend">Dans notre base de données</div>
        </div>

        <div class="stat-card">
            <h3>Utilisateurs actifs</h3>
            <div id="activeUsers" class="stat-number">Chargement...</div>
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
    // Fonction pour récupérer les données via l'API
    async function fetchData() {
        try {
            const response = await fetch('http://localhost:5000/api/statistics'); // Remplace cette URL par celle de ton API
            const data = await response.json();

            // Mettre à jour les statistiques
            document.getElementById('scansTotal').textContent = data.scansTotal;
            document.getElementById('scansTrend').textContent = data.scansTrend;
            document.getElementById('speciesIdentified').textContent = data.speciesIdentified;
            document.getElementById('activeUsers').textContent = data.activeUsers;

            // Graphiques
            updateCharts(data.speciesData, data.activityData);
        } catch (error) {
            console.error('Erreur lors de la récupération des données:', error);
        }
    }

    // Fonction pour mettre à jour les graphiques
    function updateCharts(speciesData, activityData) {
        // Graphique des espèces les plus identifiées
        const speciesCtx = document.getElementById('speciesChart').getContext('2d');
        new Chart(speciesCtx, {
            type: 'bar',
            data: {
                labels: speciesData.labels,
                datasets: [{
                    label: 'Nombre de scans',
                    data: speciesData.values,
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
                labels: activityData.labels,
                datasets: [{
                    label: 'Nombre de scans',
                    data: activityData.values,
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
    }

    // Appeler la fonction fetchData pour charger les données au chargement de la page
    fetchData();
</script>
</body>
</html>
