#Contene las configuraciones de la app v.1.4
import os

class Config:
    # Clave secreta para la aplicación
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta_super_segura')

    # Ruta de la base de datos
    basedir = os.path.abspath(os.path.dirname(__file__))
    SQLALCHEMY_DATABASE_URI = f"sqlite:///{os.path.join(basedir, 'instance', 'cumpleapp.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de correo electrónico
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True').lower() in ('true', '1', 'yes')
    MAIL_USE_SSL = os.getenv('MAIL_USE_SSL', 'False').lower() in ('true', '1', 'yes')
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')

    @staticmethod
    def validate_email_config():
        required_keys = ['MAIL_SERVER', 'MAIL_PORT', 'MAIL_USERNAME', 'MAIL_PASSWORD', 'MAIL_DEFAULT_SENDER']
        missing = [key for key in required_keys if not os.getenv(key)]
        
        if missing:
            # Imprimir todas las variables de correo para debug
            print("Estado actual de las variables de correo:")
            for key in required_keys:
                print(f"{key}: {os.getenv(key)}")
            
            raise ValueError(f"Faltan configuraciones de correo: {', '.join(missing)}")
