from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from .models import User, BlacklistedToken
from . import db

# Création du blueprint pour les différentes routes
auth_bp = Blueprint("auth", __name__)

# Enregistre le nouvel utilisateur dans la base de données
@auth_bp.route("/register", methods=["POST"])
def register():
    try:
        # Récupération des données de la requête
        data = request.get_json()
        print(f"Data reçue : {data}")  # Log des données reçues

        # Vérification des données reçues
        if not data or "username" not in data or "password" not in data:
            return jsonify({"message": "Données invalides"}), 400

        # Vérification si l'utilisateur existe déjà
        if User.query.filter_by(username=data["username"]).first():
            return jsonify({"message": "Nom d'utilisateur déjà utilisé."}), 400

        # Hashage du mot de passe
        hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")

        # Création d'un nouvel utilisateur
        new_user = User(username=data["username"], password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return jsonify({"message": "Utilisateur enregistré avec succès."}), 201
    except Exception as e:
        # Log de l'erreur pour le débogage
        print(f"Erreur lors de l'enregistrement : {e}")
        return jsonify({"message": "Erreur interne du serveur"}), 500

# Authentifie l'utilisateur si celui-ci existe dans la base de données
@auth_bp.route("/login", methods=["POST"])
def login():
    try:
        # Récupération des données de la requête
        data = request.get_json()
        print(f"Data reçue pour login : {data}")  # Log des données reçues

        # Recherche de l'utilisateur dans la base de données
        user = User.query.filter_by(username=data["username"]).first()

        # Vérification des informations d'identification
        if user and check_password_hash(user.password, data["password"]):
            # Génération d'un token JWT
            access_token = create_access_token(identity=user.username)
            return jsonify({"access_token": access_token}), 200

        print("Erreur : Nom d'utilisateur ou mot de passe incorrect")
        return jsonify({"message": "Nom d'utilisateur ou mot de passe incorrect."}), 401
    except Exception as e:
        print(f"Erreur lors de la connexion : {e}")
        return jsonify({"message": "Erreur interne du serveur"}), 500

# Fonction permettant de se déconnecter en blacklistant le token de l'utilisateur
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    try:
        # Récupérer le jeton actuel
        jti = get_jwt()['jti']  # JTI (JWT ID) est un identifiant unique pour le jeton

        # Ajouter le jeton à la liste noire
        blacklisted_token = BlacklistedToken(token=jti)
        db.session.add(blacklisted_token)
        db.session.commit()

        print("Utilisateur déconnecté avec succès")
        return jsonify({"message": "Déconnexion réussie."}), 200
    except Exception as e:
        print(f"Erreur lors de la déconnexion : {e}")
        return jsonify({"message": "Erreur interne du serveur"}), 500
