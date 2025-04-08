import mysql.connector
import os

def connect_to_database():
    try:
        connection = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="wildlens"
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database: {err}")
        return None

def load_photos():
    connection = connect_to_database()
    if not connection:
        return
    
    cursor = connection.cursor()
    
    try:
        # Get list of photos from downloaded_data/photos directory
        photos_dir = "./data/downloaded_data/Mammifères/"
        for filename in os.listdir(photos_dir):
            if filename.endswith((".jpg", ".jpeg", ".png")):
                file_path = os.path.join(photos_dir, filename)

                
                # Extract animal name from filename (assuming format: animal_name.jpg)
                animal_name = os.path.splitext(filename)[0]
                
                # Get animal_id from database
                get_animal_id = "SELECT id FROM Animal WHERE name = %s"
                cursor.execute(get_animal_id, (animal_name,))
                result = cursor.fetchone()
                
                if result:
                    animal_id = result[0]
                    
                    # Insert photo record
                    insert_query = """
                    INSERT INTO Photo (file_path, file_name, animal_id)
                    VALUES (%s, %s, %s)
                    """
                    cursor.execute(insert_query, (file_path, filename, animal_id))
                else:
                    print(f"No matching animal found for photo: {filename}")
        
        connection.commit()
        print("Successfully loaded photos into database")
        
    except Exception as e:
        print(f"Error loading photos: {e}")
        connection.rollback()
    
    finally:
        cursor.close()
        connection.close()

if __name__ == "__main__":
    load_photos()
