<!DOCTYPE html>
<head>
    <link rel="stylesheet" href="assets/CSS/find_animals.css">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" integrity="sha256-p4NxAoJBhIIN+hmNHrzRCf9tD/miZyoHS5obTRR9BMY=" crossorigin=""/>
</head>
<body>
    <div class="map-container">
        <h1 class="map-title">Où trouver les animaux ?</h1>
        
        <div class="map-controls">
            <select id="animalSelect">
                <option value="">Sélectionnez un animal</option>
                <option value="cerf">Cerf</option>
                <option value="sanglier">Sanglier</option>
                <option value="renard">Renard</option>
                <option value="chevreuil">Chevreuil</option>
                <option value="lievre">Lièvre</option>
            </select>
        </div>

        <div id="map"></div>

        <div class="animal-info">
            <h2>Informations sur l'habitat</h2>
            <p id="habitatInfo">Sélectionnez un animal pour voir ses zones d'habitat préférées.</p>
        </div>
    </div>


    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js" integrity="sha256-20nQCchB9co0qIjJZRGuk2/Z9VM+kNiyxNV1lvTlZBo=" crossorigin=""></script>
    <script>
        // Initialisation de la carte
        const map = L.map('map').setView([46.603354, 1.888334], 6); // Centre sur la France

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '© OpenStreetMap contributors'
        }).addTo(map);

        // Données exemple pour les zones d'habitat (coordonnées fictives)
        const habitatData = {
            cerf: [
                { lat: 47.0, lng: 2.0, name: "Forêt de Sologne" },
                { lat: 48.5, lng: 2.5, name: "Forêt de Fontainebleau" }
            ],
            sanglier: [
                { lat: 46.5, lng: 3.0, name: "Forêt du Morvan" },
                { lat: 45.8, lng: 1.5, name: "Parc naturel régional du Limousin" }
            ],
            renard: [
                { lat: 47.5, lng: 1.5, name: "Val de Loire" },
                { lat: 46.0, lng: 4.0, name: "Monts du Lyonnais" }
            ]
        };

        let markers = [];

        document.getElementById('animalSelect').addEventListener('change', (e) => {
            // Nettoyer les marqueurs existants
            markers.forEach(marker => map.removeLayer(marker));
            markers = [];

            const selectedAnimal = e.target.value;
            if (selectedAnimal && habitatData[selectedAnimal]) {
                habitatData[selectedAnimal].forEach(location => {
                    const marker = L.marker([location.lat, location.lng])
                        .bindPopup(location.name)
                        .addTo(map);
                    markers.push(marker);
                });

                // Mettre à jour les informations d'habitat
                const habitatInfo = {
                    cerf: "Les cerfs préfèrent les grandes forêts avec des zones de clairière. On les trouve principalement dans les massifs forestiers.",
                    sanglier: "Les sangliers s'adaptent à divers habitats, mais préfèrent les forêts mixtes avec un sous-bois dense.",
                    renard: "Le renard est très adaptable et peut vivre dans des zones rurales comme urbaines, préférant les territoires variés."
                };

                document.getElementById('habitatInfo').textContent = habitatInfo[selectedAnimal] || "Information non disponible";
            }
        });
    </script>
</body>
