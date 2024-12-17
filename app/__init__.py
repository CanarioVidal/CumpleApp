from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Inicializar extensiones
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Configuración de la aplicación
    # Usamos una variable de entorno para configurar la base de datos
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///default.db')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # Desactiva seguimiento de modificaciones (opcional)

    # Inicializar extensiones
    db.init_app(app)

    # Registrar las rutas
    with app.app_context():
        from . import routes
        db.create_all()

    return app
