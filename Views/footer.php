
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
    
    const themeToggle = document.querySelector('.icon-theme');

    themeToggle.addEventListener('click', () => {
      const html = document.documentElement;
      const currentTheme = html.getAttribute('data-theme');
      const newTheme = currentTheme === 'dark' ? 'light' : 'dark';

      html.setAttribute('data-theme', newTheme);
      localStorage.setItem('theme', newTheme);
    });

    window.addEventListener('DOMContentLoaded', () => {
    const savedTheme = localStorage.getItem('theme');
    if (savedTheme) {
      document.documentElement.setAttribute('data-theme', savedTheme);
    }
  });

    const toggleButton = document.getElementById('menu-toggle');
    const nav = document.getElementById('nav');

    toggleButton.addEventListener('click', () => {
      nav.classList.toggle('active');
    });
    
  </script>
</body>
</html>
