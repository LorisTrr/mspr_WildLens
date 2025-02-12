import pandas as pd
from sqlalchemy import create_engine, text
import re

# 🚀 Fonction 1 : Charger le fichier CSV
def load_csv(file_path):
    """Chargement des données depuis un fichier CSV"""
    # Utilisation de pandas pour charger le CSV avec un délimiteur spécifique (point-virgule)
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')

    # Nettoyage des noms de colonnes : suppression des espaces et remplacement des espaces par des underscores
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    
    # Affichage de la forme du DataFrame pour vérification
    print(f"📂 Fichier chargé : {file_path} ({df.shape[0]} lignes, {df.shape[1]} colonnes)")
    return df

# 🚀 Fonction 2 : Nettoyage du texte (guillemets mal encodés, espaces, etc.)
def nettoyer_texte(val):
    """Nettoie les caractères spéciaux et les guillemets mal encodés dans les valeurs textuelles."""
    if isinstance(val, str):
        # Remplacement des guillemets typographiques par des guillemets droits (standardisation)
        val = val.replace("«", '"').replace("»", '"').replace("“", '"').replace("”", '"')
        # Suppression des espaces insécables (\xa0)
        val = val.replace("\xa0", " ")
        # Remplacement des espaces multiples par un seul espace et suppression des espaces en début et fin de chaîne
        val = re.sub(r"\s+", " ", val).strip()
    return val

# 🚀 Fonction 3 : Nettoyage des données
def clean_data(df):
    """Effectue le nettoyage et la transformation des données."""
    
    # Remplacement de toutes les valeurs manquantes (NaN) par "Information non renseignée"
    df.fillna("Information non renseignée", inplace=True)
    df.replace("", "Information non renseignée", inplace=True)

    # Applique la fonction de nettoyage des textes sur toutes les colonnes du DataFrame
    df = df.applymap(nettoyer_texte)

    # ✅ Traitement spécifique pour la colonne "Taille"
    def convertir_taille(val):
        """Convertir les valeurs de taille en mètres."""
        if isinstance(val, str):
            # Retrait des espaces insécables
            val = val.replace("\xa0", " ")
            # Vérifier si la taille est en centimètres
            if 'cm' in val:
                # Extraction des valeurs numériques de taille (ex: "100 à 135 cm")
                tailles = re.findall(r'\d+', val)
                if len(tailles) == 2:
                    # Si deux tailles sont trouvées, on suppose une plage (min-max)
                    taille_min = float(tailles[0]) / 100  # Conversion en mètres
                    taille_max = float(tailles[1]) / 100  # Conversion en mètres
                    return f"{taille_min:.2f} m à {taille_max:.2f} m"
                elif len(tailles) == 1:
                    # Si une seule taille est donnée, conversion directe
                    return f"{float(tailles[0]) / 100:.2f} m"
        
        return "Information non renseignée"  # Retour par défaut si la conversion échoue

    # Appliquer la conversion à la colonne "Taille"
    df["Taille"] = df["Taille"].apply(convertir_taille)

    # ✅ Suppression des chiffres dans toutes les colonnes sauf "Taille"
    def supprimer_chiffres(val):
        """Supprime tous les chiffres d'une chaîne de caractères sauf pour la colonne 'Taille'."""
        return re.sub(r"\d+", "", val) if isinstance(val, str) else val
    
    # Appliquer la suppression des chiffres dans toutes les colonnes sauf "Taille"
    for col in df.columns:
        if col != "Taille":
            df[col] = df[col].apply(supprimer_chiffres)

    # ✅ Normalisation de la colonne "Région"
    df["Région"] = df["Région"].str.replace(",", ";").str.replace("  ", " ").str.strip()

    # Affichage pour confirmer que les données ont été nettoyées et standardisées
    print("✅ Données nettoyées et standardisées !")
    return df

# 🚀 Fonction 4 : Connexion à la base de données MySQL
def connect_to_db():
    """Établit une connexion à la base de données MySQL."""
    # Création d'une connexion à la base de données avec SQLAlchemy
    engine = create_engine("mysql+mysqlconnector://root:@localhost/wildlens")
    print("✅ Connexion réussie à la base de données !")
    return engine

# 🚀 Fonction 5 : Insertion des données dans MySQL
def insert_data(df, engine, table_name="animal"):
    """Insère les données nettoyées dans la base de données MySQL."""
    try:
        # Désactivation temporaire des clés étrangères pour éviter les conflits lors de l'insertion
        with engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            conn.execute(text("TRUNCATE TABLE photo"))
            conn.execute(text("TRUNCATE TABLE animal"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            conn.commit()

        # Insertion des données dans la table spécifiée, en mode 'append' (ajout)
        df.to_sql(table_name, con=engine, if_exists='append', index=False)
        print(f"✅ Données insérées dans la table `{table_name}` !")
    except Exception as e:
        # En cas d'erreur lors de l'insertion
        print(f"❌ Erreur d'insertion : {e}")

# 🚀 Exécution du script principal
if __name__ == "__main__":
    # Chemin vers le fichier CSV contenant les données des espèces
    csv_file = "downloaded_data/infos_especes.csv"  # Mettre ici le chemin exact de ton fichier

    # Chargement du fichier CSV dans un DataFrame
    df = load_csv(csv_file)
    
    # Nettoyage des données
    df = clean_data(df)
    
    # Connexion à la base de données
    engine = connect_to_db()
    
    # Insertion des données dans la table MySQL
    insert_data(df, engine)
