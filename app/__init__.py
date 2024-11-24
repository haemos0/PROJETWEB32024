from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from flask_cors import CORS  # Ajout de CORS pour permettre l'interaction avec un frontend moderne

# Initialisation des outils et extensions
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

# Fonction pour vérifier si un token JWT est blacklisté
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    from .models import BlacklistedToken  # Import local pour éviter les imports circulaires
    jti = jwt_payload['jti']
    return db.session.query(db.exists().where(BlacklistedToken.token == jti)).scalar()

# Fonction de création de l'application
def create_app():
    app = Flask(__name__)
    
    # Configuration de l'application
    app.config.from_object("config.Config")  # Charger la configuration depuis config.py
    
    # Initialisation des extensions
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    CORS(app)  # Activer les CORS pour permettre les requêtes frontend-backend
    
    # Enregistrement des blueprints
    with app.app_context():
        from .routes import main_bp
        from .auth import auth_bp
        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)

        # Import des modèles avant création des tables
        from . import models
        db.create_all()

    return app
