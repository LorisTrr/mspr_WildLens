from flask import Flask, request, jsonify, session
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import os
import re
import numpy as np
import tensorflow as tf
from tensorflow.keras.preprocessing import image
from PIL import Image
import io
import uuid
import logging
from datetime import datetime

# === Configuration ===
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.secret_key = "votre_clé_ultra_secrète"
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost/wildlens'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# === Logger ===
logging.basicConfig(
    filename="api/wildlens_api.log",
    level=logging.ERROR,
    format='%(asctime)s [%(levelname)s] Route: %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

def log_error(route_name, error):
    logging.error(f"{route_name} | Exception: {str(error)}")

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
    access_token = db.Column(db.String(255))
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

# === Routes ===
@app.route('/logout', methods=['GET'])
def logout():
    session.clear()
    return jsonify({'message': 'Déconnecté'})

@app.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        email = data.get('email')
        password = data.get('password')

        user = User.query.filter_by(email=email).first()
        if not user or not check_password_hash(user.password, password):
            return jsonify({'error': 'Identifiants invalides'}), 401

        token = str(uuid.uuid4())
        user.access_token = token
        db.session.commit()

        return jsonify({
            'access_token': token,
            'id': user.id,
            'username': user.username
        })
    except Exception as e:
        log_error('/login', e)
        return jsonify({'error': str(e)}), 500

@app.route('/reset-password-direct', methods=['POST'])
def reset_password_direct():
    try:
        data = request.get_json()
        email = data.get('email')
        new_password = data.get('password')

        if not email or not new_password or len(new_password) < 6:
            return jsonify({'error': "Champs invalides"}), 400

        user = User.query.filter_by(email=email).first()
        if not user:
            return jsonify({'error': "Email non trouvé"}), 404

        user.password = generate_password_hash(new_password)
        db.session.commit()

        return jsonify({'message': "Mot de passe mis à jour avec succès"})
    except Exception as e:
        log_error('/reset-password-direct', e)
        return jsonify({'error': str(e)}), 500

@app.route('/users', methods=['POST'])
def register_user():
    try:
        data = request.get_json()
        required_fields = ['username', 'email', 'password']

        if not data or not all(field in data and data[field].strip() for field in required_fields):
            return jsonify({'error': 'Champs requis manquants ou vides'}), 400

        if not EMAIL_REGEX.match(data['email']):
            return jsonify({'error': 'Email invalide'}), 400

        if len(data['password']) < 6:
            return jsonify({'error': 'Mot de passe trop court'}), 400

        if User.query.filter_by(email=data['email']).first():
            return jsonify({'error': 'Email déjà utilisé'}), 409

        hashed_password = generate_password_hash(data['password'])
        user = User(
            username=data['username'].strip(),
            email=data['email'].strip(),
            password=hashed_password,
            first_name=data.get('first_name', '').strip(),
            last_name=data.get('last_name', '').strip()
        )
        db.session.add(user)
        db.session.commit()

        return jsonify({'message': 'Utilisateur enregistré', 'id': user.id}), 201
    except Exception as e:
        log_error('/users', e)
        return jsonify({'error': str(e)}), 500

@app.route('/users/<int:id>', methods=['PUT'])
def update_user(id):
    try:
        token = request.headers.get('Authorization', '').replace('Bearer ', '')
        user = User.query.filter_by(id=id, access_token=token).first()

        if not user:
            return jsonify({'error': 'Accès interdit'}), 403

        data = request.get_json()
        user.username = data.get('username', user.username)
        user.email = data.get('email', user.email)
        db.session.commit()

        return jsonify({'message': 'Utilisateur mis à jour'}), 200
    except Exception as e:
        log_error('/users/<id>', e)
        return jsonify({'error': str(e)}), 500

@app.route('/photos/user', methods=['GET'])
def get_user_photos():
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Non autorisé'}), 403

        photos = Photo.query.filter_by(user_id=session['user_id']).all()
        return jsonify([{
            'file_name': p.file_name,
            'file_path': p.file_path,
            'upload_date': p.upload_date.isoformat()
        } for p in photos])
    except Exception as e:
        log_error('/photos/user', e)
        return jsonify({'error': str(e)}), 500

@app.route('/photos/<int:id>', methods=['GET'])
def get_photo_by_id(id):
    try:
        if 'user_id' not in session:
            return jsonify({'error': 'Non autorisé'}), 403

        photo = Photo.query.get_or_404(id)
        if photo.user_id != session['user_id']:
            return jsonify({'error': 'Accès interdit à cette photo'}), 403

        return jsonify({
            'id': photo.id,
            'file_name': photo.file_name,
            'file_path': photo.file_path,
            'upload_date': photo.upload_date.isoformat()
        })
    except Exception as e:
        log_error('/photos/<id>', e)
        return jsonify({'error': str(e)}), 500

@app.route('/scan-history', methods=['GET'])
def get_user_scan_history():
    try:
        user_id = session.get('user_id') or request.args.get('user_id')
        if not user_id:
            return jsonify({'error': 'Non autorisé'}), 403

        scans = ScanHistory.query.filter_by(user_id=user_id).all()
        return jsonify([{
            'photo_id': s.photo_id,
            'scan_date': s.scan_date.isoformat()
        } for s in scans])
    except Exception as e:
        log_error('/scan-history', e)
        return jsonify({'error': str(e)}), 500

@app.route('/model/predict', methods=['POST'])
def predict():
    try:
        if 'file' not in request.files:
            return jsonify({'error': 'Aucun fichier envoyé'}), 400

        file = request.files['file']
        if file.filename == '':
            return jsonify({'error': 'Nom de fichier vide'}), 400

        img = Image.open(io.BytesIO(file.read())).convert("RGB")
        img = img.resize((224, 224))
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
        else:
            return jsonify({'message': 'Animal non reconnu'}), 200
    except Exception as e:
        log_error('/model/predict', e)
        return jsonify({'error': str(e)}), 500

@app.route('/animals', methods=['GET'])
def get_animals():
    try:
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
    except Exception as e:
        log_error('/animals', e)
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
