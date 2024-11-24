from flask import Blueprint, jsonify

# Création du blueprint pour toutes les routes de l'application
main_bp = Blueprint("main", __name__)

# Point d'accès de l'API
@main_bp.route("/api", methods=["GET"])
def index():
    return jsonify({"message": "test"})
