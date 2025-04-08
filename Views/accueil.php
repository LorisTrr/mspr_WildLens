<head>
    <link rel="stylesheet" href="assets/CSS/accueil.css">
</head>
<body>
    
    <div class="container">
        <h1>Scannez une trace de pas !</h1>
        <div class="scanimage">
            <div class="image">
                <img class="phone" src="assets/images/phone.png" alt="">
            </div>
            <div class="form">
                <p>A partir de notre site web, vous pouvez importer une photo depuis votre ordinateur</p>
                <p>Choisissez votre photo dans votre gallerie d'image</p>
                <form method="POST" enctype="multipart/form-data">
                    <div class="file-upload">
                        <label for="fileInput" class="file-label">
                        <span class="file-button">Choisir un fichier</span>
                        <span class="file-text">Aucun fichier sélectionné</span>
                        <input type="file" id="fileInput" name='file' class="file-input">
                        </label>
                        <br/>
                        <input type="text" class="city" placeholder="Quel est la ville la plus proche de l'empreinte" name='city' />
                        <br/>
                        <button type="submit" class="file-button">Envoyer</button>
                    </div>
                </form>
            </div>
        </div>
    </div>
</body>


<script>
  const fileInput = document.getElementById('fileInput');
  const fileText = document.querySelector('.file-text');

  fileInput.addEventListener('change', function() {
    if (fileInput.files.length > 0) {
      fileText.textContent = fileInput.files[0].name;
    } else {
      fileText.textContent = "Aucun fichier sélectionné";
    }
  });
</script>
