<?php
    $url = "http://127.0.0.1:5000/animals";

    $ch = curl_init();
    curl_setopt($ch, CURLOPT_URL, $url);
    curl_setopt($ch, CURLOPT_RETURNTRANSFER, true);
    $response = curl_exec($ch);
    curl_close($ch);
    $animals = json_decode($response, true);
?>
<head>
    <link rel="stylesheet" href="CSS/animals.css">
</head>

<body>
    <div class="container">
        <?php if ($animals != null) { ?>
        <div class="tab_animals">
            <?php
                foreach($animals as $animal){  ?>
                    <div class="animal">
                        <img src="assets/images/<?php echo $animal['espece'] ; ?>.png" alt="Photo <?php echo $animal['espece'] ; ?> " class="animal_picture">
                        <a class='link_animal' href="#animal_<?php echo $animal['id'] ; ?>"> <h3 class="name-animal"><?php echo $animal['espece'] ?></h3></a>
                    </div>
                <?php }
            ?>
            
        </div>
        <?php 
        foreach($animals as $animal){ ?>
        <div id='animal_<?php echo $animal['id']; ?>' class="category">
            <div class="title-img">
                <img src="assets/images/<?php echo $animal['espece']; ?>.png" alt="Photo <?php echo $animal['espece']; ?>" class="animal">
                <h3><?php echo $animal['espece']; ?></h3>
            </div>
        
            <div class="description">
            <span style='font-size: bold;'> Espece :</span><?php echo $animal['espece'] ; ?><br><br>
            <span style='font-size: bold;'> Habitat :</span><?php echo $animal['habitat'] ; ?><br><br>
            <span style='font-size: bold;'> Famille :</span><?php echo $animal['famille'] ; ?><br><br>
            <span style='font-size: bold;'>Nom latin : </span><?php echo $animal['nom_latin'] ; ?><br><br>
            Description : <?php echo $animal['description'] ; ?><br><br>
            <span style='font-size: bold;'>Fun fact :</span> <?php echo $animal['fun_fact']; ?><br><br>
            </div>
        </div>
        <?php }}else{ ?>
            <div class="no-animals">Aucune espèces n'a encore été ajoutée</div>
        <?php } ?>
    </div>
</body>