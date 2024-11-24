from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_jwt_extended import JWTManager
from .models import User, BlacklistedToken

# Initialisation de la db et du token manager
db = SQLAlchemy()
migrate = Migrate()
jwt = JWTManager()

"""
Vérifie si le token est blacklisté (logout) 

:param jwt_header: Header du token
:param jwt_payload: Payload du token
:return: True si token blacklisté, sinon false
"""
@jwt.token_in_blocklist_loader
def check_if_token_in_blacklist(jwt_header, jwt_payload):
    jti = jwt_payload['jti']
    return BlacklistedToken.query.filter_by(token=jti).first() is not None

"""
créationde l'application

:return: une instance de l'application
"""
def create_app():
    app = Flask(__name__)
    app.config.from_object("config.Config")
    db.init_app(app)
    jwt.init_app(app)
    migrate.init_app(app, db)
    
    with app.app_context():
        from .routes import main_bp
        from .auth import auth_bp

        app.register_blueprint(main_bp)
        app.register_blueprint(auth_bp)

        db.create_all()
    return app
