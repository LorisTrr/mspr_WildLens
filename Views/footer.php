
<head>
  <link rel="stylesheet" href="assets/CSS/footer.css">
</head>
<body>
  <div class="content">
    <!-- Contenu principal de la page -->
  </div>

  <footer>
    <div class="footer-container">
      <p class="footer-text">© 2024 Mon Site Web. Tous droits réservés.</p>
      <ul class="footer-links">
        <li><a href="#">Mentions légales</a></li>
        <li><a href="#">Politique de confidentialité</a></li>
        <li><a href="#">Contact</a></li>
      </ul>
      <div class="footer-social">
        <a href="#" class="social-icon">Facebook</a>
        <a href="#" class="social-icon">Twitter</a>
        <a href="#" class="social-icon">Instagram</a>
      </div>
    </div>
  </footer>
  <script>
    
    const toggleTheme = () => {
    const current = document.documentElement.getAttribute('data-theme')
    document.documentElement.setAttribute('data-theme', current === 'dark' ? 'light' : 'dark')
    }
    button = document.querySelector('.icon-theme')
    button.addEventListener('click', toggleTheme)
    
  </script>
</body>
</html>
