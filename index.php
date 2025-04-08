<?php 
session_start();
$is_logged_in = isset($_SESSION['user_email']) ? true : false;


require_once "Views/header.php";

$page = 'accueil';

if(isset($_GET['page'])){
    $page = $_GET['page'];
}

if (
    isset($_POST['city'], $_FILES['file']) && // Vérifie si les 2 existent
    !empty(trim($_POST['city'])) &&           // Vérifie que city n'est pas vide (même sans espaces)
    $_FILES['file']['error'] === 0            // Vérifie qu'il y a bien un fichier uploadé sans erreur
) {
    $page = 'predict';
}elseif ($page == ''){
    $page = 'accueil';
}


switch($page) {
    case 'animale':
        require_once "Views/animales.php";
        break;
    case 'accueil':
        require_once "Views/accueil.php";
        break;
    case 'stat':
        require_once "Views/stat.php";
        break;
    case 'findanimals':
        require_once "Views/find_animals.php";
        break;
    case 'log' : 
        require_once "Views/log.php";
        break;
    case 'predict':
        require_once "Views/predict.php";
        break;
    default:
        require_once "Views/accueil.php";
        break;

}

//require_once "Views/accueil.php";
require_once "Views/footer.php";
