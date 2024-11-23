from flask import Blueprint, jsonify

main_bp = Blueprint("main", __name__)

@main_bp.route("/api", methods=["GET"])
def index():
    return jsonify({"message": "test"})
