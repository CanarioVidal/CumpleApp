from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv
import os
from settings import Config

# Cargar variables de entorno
load_dotenv()

# Inicializar extensiones
db = SQLAlchemy()
mail = Mail()

def create_app():
    """Crear y configurar la aplicación Flask."""
    app = Flask(__name__)
    
    # Cargar configuración desde el archivo settings.py
    app.config.from_object(Config)
    
    # Inicializar extensiones con la app
    db.init_app(app)
    mail.init_app(app)
    
    # Registrar blueprints
    from .routes import routes
    app.register_blueprint(routes)

    # Configuración de tareas programadas
    with app.app_context():
        # Crear tablas si no existen
        db.create_all()

        # Importar y configurar tareas programadas
        from app.tasks import iniciar_tareas
        iniciar_tareas()

    return app
