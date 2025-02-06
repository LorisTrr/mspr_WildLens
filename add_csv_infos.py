import pandas as pd
from sqlalchemy import create_engine, text

# 1️⃣ Charger le fichier CSV
def load_csv(file_path):
    df = pd.read_csv(file_path, delimiter=';', encoding='utf-8')
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    

    print("Aperçu des données :")
    print(df.head())
    return df

# 2️⃣ Connexion à MySQL
def connect_to_db():    
    engine = create_engine(f"mysql+mysqlconnector://{'root'}:{''}@{'localhost'}/{'wildlens'}")
    print("✅ Connexion réussie à la base de données !")
    return engine

# 3️⃣ Insérer les données dans MySQL
def insert_data(df, engine, table_name="Animal"):
    try:
        # First truncate the photo table to remove foreign key constraints
        with engine.connect() as conn:
            conn.execute(text("SET FOREIGN_KEY_CHECKS=0"))
            conn.execute(text("TRUNCATE TABLE photo"))
            conn.execute(text("TRUNCATE TABLE animal"))
            conn.execute(text("SET FOREIGN_KEY_CHECKS=1"))
            conn.commit()
            
        # Now we can safely insert the data
        df.to_sql('animal', con=engine, if_exists='append', index=False)
        print(f"✅ Données insérées dans la table {table_name}!")
    except Exception as e:
        print(f"❌ Erreur d'insertion : {e}")



# 🚀 Exécution des étapes
csv_file = "downloaded_data/infos_especes.csv"  # Remplace par ton chemin correct
df = load_csv(csv_file)
engine = connect_to_db()
insert_data(df, engine)