from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
from .models import User, BlacklistedToken
from . import db

# Création du blueprint pour les différentes routes
auth_bp = Blueprint("auth", __name__)


# Enregistre le nouveau utilisateur dans la base de données
@auth_bp.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    hashed_password = generate_password_hash(data["password"], method="pbkdf2:sha256")
    new_user = User(username=data["username"], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "Utilisateur enregistré avec succès."}), 201

# Authentifie l'utilisateur si celui-ci existe dans la base de données
@auth_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data["username"]).first()
    if user and check_password_hash(user.password, data["password"]):
        access_token = create_access_token(identity=user.username)
        return jsonify({"access_token": access_token}), 200
    return jsonify({"message": "Nom d'utilisateur ou mot de passe incorrect."}), 401

# Fonction permettant de se déconnecter en blacklistant le token de l'utilisateur
@auth_bp.route("/logout", methods=["POST"])
@jwt_required()
def logout():
    # Récupérer le jeton actuel
    jti = get_jwt()['jti']  # JTI (JWT ID) est un identifiant unique pour le jeton
    
    # Ajouter le jeton à la liste noire
    blacklisted_token = BlacklistedToken(token=jti)
    db.session.add(blacklisted_token)
    db.session.commit()

    return jsonify({"message": "Déconnexion réussie."}), 200