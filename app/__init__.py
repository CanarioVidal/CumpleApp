from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os
from settings import Config

# Cargar variables de entorno
load_dotenv()

db = SQLAlchemy()

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Inicializar base de datos
    db.init_app(app)

    # Registrar rutas con Blueprint
    from .routes import routes
    app.register_blueprint(routes)

    # Crear tablas si no existen
    with app.app_context():
        db.create_all()

    return app
