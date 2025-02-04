# Configura la app Flask y conecta los módulos necesarios. v.1.8
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail
from dotenv import load_dotenv, find_dotenv
from settings import Config
import os

#Definir from
MAIL_DEFAULT_SENDER = '"The End, un bar de amigos" <hola@theend.com.uy>'


# Cargar variables de entorno
if not load_dotenv(find_dotenv()):
    print("No se pudo cargar el archivo .env")
else:
    print("Archivo .env cargado correctamente")

# Inicializar extensiones
db = SQLAlchemy()
mail = Mail()

def create_app():
    """Crear y configurar la aplicación Flask."""
    app = Flask(__name__)
    
    # Cargar configuración desde el archivo settings.py
    app.config.from_object(Config) 
    
    # Depuración: imprimir las configuraciones de correo cargadas
    print("=== Configuración de correo cargada ===")
    for key in ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USE_TLS', 'MAIL_USE_SSL', 'MAIL_USERNAME', 'MAIL_PASSWORD', 'MAIL_DEFAULT_SENDER']:
        print(f"{key}: {os.getenv(key)}")
    
    # Validar configuraciones de correo electrónico
    try:
        Config.validate_email_config()
    except ValueError as e:
        print(f"Error en la configuración de correo: {e}")
        raise

    # Inicializar extensiones con la app
    db.init_app(app)
    mail.init_app(app)
    
    # Registrar blueprints
    from .routes import routes  # Importación local para evitar problemas circulares
    app.register_blueprint(routes)

    # Configuración de tareas programadas
    with app.app_context():
        # Crear tablas si no existen
        from app.models import User  # Importación local para evitar referencias circulares
        db.create_all()

        # Inicializar tareas programadas con la instancia de la app
        from app.tasks import iniciar_tareas  # Importar aquí para evitar importaciones circulares
        iniciar_tareas(app)

    return app
