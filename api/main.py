from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
import tensorflow as tf
import numpy as np
import os
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
CORS(app)


# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/wildlens'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
model = tf.keras.models.load_model('model/model_trained.h5')


with open('model/class_names.txt', 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

# Modèles
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    first_name = db.Column(db.String(50))
    last_name = db.Column(db.String(50))
    created_at = db.Column(db.DateTime, default=db.func.current_timestamp())

class Animal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    espece = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text)
    nom_latin = db.Column(db.String(100))
    famille = db.Column(db.String(50))
    taille = db.Column(db.String(50))
    region = db.Column(db.String(100))
    habitat = db.Column(db.Text)
    fun_fact = db.Column(db.Text)

class Location(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    country = db.Column(db.String(100), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    latitude = db.Column(db.Numeric(10, 8))
    longitude = db.Column(db.Numeric(11, 8))

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))

class ScanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    location_id = db.Column(db.Integer, db.ForeignKey('location.id'), nullable=False)
    scan_date = db.Column(db.DateTime, default=db.func.current_timestamp())

# Routes CRUD pour les utilisateurs
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{
        'id': u.id,
        'username': u.username,
        'email': u.email,
        'first_name': u.first_name,
        'last_name': u.last_name,
        'created_at': u.created_at
    } for u in users])



@app.route('/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(
        username=data['username'],
        email=data['email'],
        password=data['password'],
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur ajouté avec succès'}), 201

# Route pour se connecter
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data['email']).first()
    if user and user.password == data['password']:
        return jsonify({
            'id': user.id,
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'created_at': user.created_at
        })
    
    return jsonify({'message': 'Nom d\'utilisateur ou mot de passe incorrect'}), 401
@app.route('/model/predict', methods=['POST'])
def predict():
    data = request.get_json()
    path = data['path']

    try:
        # Charger et préparer l'image
        img = image.load_img(path, target_size=(150, 150))
        img_array = image.img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array /= 255.0  # Normalisation comme pendant le training

        # Prédiction
        prediction = model.predict(img_array)
        predicted_class = class_names[np.argmax(prediction[0])]
        # get animal from name
        animal = Animal.query.filter_by(espece=predicted_class).first()
        if animal:
            animal_info = {
                'id': animal.id,
                'espece': animal.espece,
                'description': animal.description,
                'nom_latin': animal.nom_latin,
                'famille': animal.famille,
                'taille': animal.taille,
                'region': animal.region,
                'habitat': animal.habitat,
                'fun_fact': animal.fun_fact
            }
        else:
            animal_info = None

        return jsonify(animal_info), 200

    except Exception as e:
        return jsonify({'error': str(e)})

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    data = request.get_json()
    user = User.query.get_or_404(id)
    user.username = data.get('username', user.username)
    user.email = data.get('email', user.email)
    user.password = data.get('password', user.password)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    db.session.commit()
    return jsonify({'message': 'Utilisateur mis à jour avec succès'})

@app.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur supprimé avec succès'})

# Routes CRUD pour les animaux
@app.route('/animals', methods=['GET'])
def get_animals():
    animals = Animal.query.all()
    return jsonify([{
        'id': a.id,
        'espece': a.espece,
        'description': a.description,
        'nom_latin': a.nom_latin,
        'famille': a.famille,
        'taille': a.taille,
        'region': a.region,
        'habitat': a.habitat,
        'fun_fact': a.fun_fact
    } for a in animals])

@app.route('/animals', methods=['POST'])
def add_animal():
    data = request.get_json()
    new_animal = Animal(
        espece=data['espece'],
        description=data.get('description', ''),
        nom_latin=data.get('nom_latin', ''),
        famille=data.get('famille', ''),
        taille=data.get('taille', ''),
        region=data.get('region', ''),
        habitat=data.get('habitat', ''),
        fun_fact=data.get('fun_fact', '')
    )
    db.session.add(new_animal)
    db.session.commit()
    return jsonify({'message': 'Animal ajouté avec succès'}), 201

@app.route('/animals/<int:id>', methods=['PUT'])
def update_animal(id):
    data = request.get_json()
    animal = Animal.query.get_or_404(id)
    animal.espece = data.get('espece', animal.espece)
    animal.description = data.get('description', animal.description)
    animal.nom_latin = data.get('nom_latin', animal.nom_latin)
    animal.famille = data.get('famille', animal.famille)
    animal.taille = data.get('taille', animal.taille)
    animal.region = data.get('region', animal.region)
    animal.habitat = data.get('habitat', animal.habitat)
    animal.fun_fact = data.get('fun_fact', animal.fun_fact)
    db.session.commit()
    return jsonify({'message': 'Animal mis à jour avec succès'})

@app.route('/animals/<int:id>', methods=['DELETE'])
def delete_animal(id):
    animal = Animal.query.get_or_404(id)
    db.session.delete(animal)
    db.session.commit()
    return jsonify({'message': 'Animal supprimé avec succès'})

# Routes CRUD pour les photos
@app.route('/photos', methods=['GET'])
def get_photos():
    photos = Photo.query.all()
    return jsonify([{
        'id': p.id,
        'file_path': p.file_path,
        'file_name': p.file_name,
        'upload_date': p.upload_date,
        'animal_id': p.animal_id
    } for p in photos])

@app.route('/photos', methods=['POST'])
def add_photo():
    data = request.get_json()
    new_photo = Photo(
        file_path=data['file_path'],
        file_name=data['file_name'],
        animal_id=data['animal_id']
    )
    db.session.add(new_photo)
    db.session.commit()
    return jsonify({'message': 'Photo ajoutée avec succès'}), 201

@app.route('/photos/<int:id>', methods=['PUT'])
def update_photo(id):
    data = request.get_json()
    photo = Photo.query.get_or_404(id)
    photo.file_path = data.get('file_path', photo.file_path)
    photo.file_name = data.get('file_name', photo.file_name)
    photo.animal_id = data.get('animal_id', photo.animal_id)
    db.session.commit()
    return jsonify({'message': 'Photo mise à jour avec succès'})

@app.route('/photos/<int:id>', methods=['DELETE'])
def delete_photo(id):
    photo = Photo.query.get_or_404(id)
    db.session.delete(photo)
    db.session.commit()
    return jsonify({'message': 'Photo supprimée avec succès'})

# Routes CRUD pour les historiques de scan
@app.route('/scan-history', methods=['GET'])
def get_scan_history():
    scans = ScanHistory.query.all()
    return jsonify([{
        'id': s.id,
        'photo_id': s.photo_id,
        'user_id': s.user_id,
        'location_id': s.location_id,
        'scan_date': s.scan_date
    } for s in scans])

@app.route('/scan-history', methods=['POST'])
def add_scan_history():
    data = request.get_json()
    new_scan = ScanHistory(
        photo_id=data['photo_id'],
        user_id=data['user_id'],
        location_id=data['location_id']
    )
    db.session.add(new_scan)
    db.session.commit()
    return jsonify({'message': 'Historique de scan ajouté avec succès'}), 201

@app.route('/scan-history/<int:id>', methods=['PUT'])
def update_scan_history(id):
    data = request.get_json()
    scan = ScanHistory.query.get_or_404(id)
    scan.photo_id = data.get('photo_id', scan.photo_id)
    scan.user_id = data.get('user_id', scan.user_id)
    scan.location_id = data.get('location_id', scan.location_id)
    db.session.commit()
    return jsonify({'message': 'Historique de scan mis à jour avec succès'})

@app.route('/scan-history/<int:id>', methods=['DELETE'])
def delete_scan_history(id):
    scan = ScanHistory.query.get_or_404(id)
    db.session.delete(scan)
    db.session.commit()
    return jsonify({'message': 'Historique de scan supprimé avec succès'})

# Routes CRUD pour les locations
@app.route('/locations', methods=['GET'])
def get_locations():
    locations = Location.query.all()
    return jsonify([{
        'id': loc.id,
        'country': loc.country,
        'city': loc.city,
        'latitude': loc.latitude,
        'longitude': loc.longitude
    } for loc in locations])


@app.route('/locations', methods=['POST'])
def add_location():
    data = request.get_json()
    new_location = Location(
        country=data['country'],
        city=data['city'],
        latitude=data.get('latitude', None),
        longitude=data.get('longitude', None)
    )
    db.session.add(new_location)
    db.session.commit()
    return jsonify({'message': 'Emplacement ajouté avec succès'}), 201

@app.route('/locations/<int:id>', methods=['PUT'])
def update_location(id):
    data = request.get_json()
    location = Location.query.get_or_404(id)
    location.country = data.get('country', location.country)
    location.city = data.get('city', location.city)
    location.latitude = data.get('latitude', location.latitude)
    location.longitude = data.get('longitude', location.longitude)
    db.session.commit()
    return jsonify({'message': 'Emplacement mis à jour avec succès'})

@app.route('/locations/<int:id>', methods=['DELETE'])
def delete_location(id):
    location = Location.query.get_or_404(id)
    db.session.delete(location)
    db.session.commit()
    return jsonify({'message': 'Emplacement supprimé avec succès'})

# Lancer l'application dans le bon contexte
if __name__ == '__main__':
    with app.app_context():  # Crée le contexte d'application
        db.create_all()  # Crée toutes les tables
    app.run(debug=False)
