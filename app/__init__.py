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

    # Registrar rutas manualmente
    with app.app_context():
        from . import routes
        db.create_all()

    return app
