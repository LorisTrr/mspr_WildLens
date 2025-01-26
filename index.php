<?php 

require_once "Views/header.php";

$page = 'accueil';

if(isset($_GET['page'])){
    $page = $_GET['page'];
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
    default:
        require_once "Views/accueil.php";
        break;

}

//require_once "Views/accueil.php";
require_once "Views/footer.php";
