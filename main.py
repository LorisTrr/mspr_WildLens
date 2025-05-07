from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image

app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "votre_clé_ultra_secrète"

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/wildlens'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# === Modèle IA ===
model = tf.keras.models.load_model('model/model_trained.h5')
with open('model/class_names.txt', 'r') as f:
    class_names = [line.strip() for line in f.readlines()]

# === Modèles ===
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

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    file_path = db.Column(db.String(255), nullable=False)
    file_name = db.Column(db.String(255), nullable=False)
    upload_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    animal_id = db.Column(db.Integer, db.ForeignKey('animal.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)


class ScanHistory(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    photo_id = db.Column(db.Integer, db.ForeignKey('photo.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    scan_date = db.Column(db.DateTime, default=db.func.current_timestamp())

EMAIL_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

# === Auth ===
@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(email=data.get('email')).first()
    if user and check_password_hash(user.password, data.get('password')):
        session['user_id'] = user.id
        return jsonify({'message': 'Connecté', 'id': user.id})
    return jsonify({'error': 'Identifiants incorrects'}), 401

@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({'message': 'Déconnecté'})

# === CRUD Utilisateur ===
@app.route('/users', methods=['POST'])
def register_user():
    data = request.get_json()
    if not data or not EMAIL_REGEX.match(data['email']):
        return jsonify({'error': 'Email invalide'}), 400
    if len(data['password']) < 6:
        return jsonify({'error': 'Mot de passe trop court'}), 400
    if User.query.filter_by(email=data['email']).first():
        return jsonify({'error': 'Email déjà utilisé'}), 409

    hashed = generate_password_hash(data['password'])
    user = User(
        username=data['username'],
        email=data['email'],
        password=hashed,
        first_name=data.get('first_name', ''),
        last_name=data.get('last_name', '')
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({'message': 'Utilisateur créé'}), 201

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    if 'user_id' not in session or session['user_id'] != id:
        return jsonify({'error': 'Accès interdit'}), 403

    user = User.query.get_or_404(id)
    data = request.get_json()
    user.username = data.get('username', user.username)
    user.first_name = data.get('first_name', user.first_name)
    user.last_name = data.get('last_name', user.last_name)
    db.session.commit()
    return jsonify({'message': 'Utilisateur mis à jour'})

# === Photos de l'utilisateur ===
@app.route('/photos/user', methods=['GET'])
def get_user_photos():
    if 'user_id' not in session:
        return jsonify({'error': 'Non autorisé'}), 403
    photos = Photo.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        'file_name': p.file_name,
        'file_path': p.file_path,
        'upload_date': p.upload_date.isoformat()
    } for p in photos])

# === ScanHistory de l'utilisateur ===
@app.route('/scan-history', methods=['GET'])
def get_user_scan_history():
    if 'user_id' not in session:
        return jsonify({'error': 'Non autorisé'}), 403
    scans = ScanHistory.query.filter_by(user_id=session['user_id']).all()
    return jsonify([{
        'photo_id': s.photo_id,
        'scan_date': s.scan_date.isoformat()
    } for s in scans])

# === Prédiction IA ===
@app.route('/model/predict', methods=['POST'])
def predict():
    data = request.get_json()
    path = data.get('path')
    if not path or not os.path.exists(path):
        return jsonify({'error': 'Fichier non trouvé'}), 400

    img = image.load_img(path, target_size=(150, 150))
    img_array = image.img_to_array(img)
    img_array = np.expand_dims(img_array, axis=0) / 255.0
    prediction = model.predict(img_array)
    predicted_class = class_names[np.argmax(prediction[0])]
    animal = Animal.query.filter_by(espece=predicted_class).first()
    if animal:
        return jsonify({
            'espece': animal.espece,
            'description': animal.description,
            'nom_latin': animal.nom_latin,
            'famille': animal.famille,
            'taille': animal.taille,
            'region': animal.region,
            'habitat': animal.habitat,
            'fun_fact': animal.fun_fact
        })
    return jsonify({'message': 'Animal non reconnu'}), 404

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
