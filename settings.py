#Contene las configuraciones de la app v.1.0
import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta_super_segura')

    # Configuración FIJA para asegurar la ruta absoluta
    SQLALCHEMY_DATABASE_URI = 'sqlite:///E:/cumpleapp/instance/cumpleapp.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Configuración de correo electrónico
    MAIL_SERVER = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
    MAIL_PORT = int(os.getenv('MAIL_PORT', 587))
    MAIL_USE_TLS = os.getenv('MAIL_USE_TLS', 'True') == 'True'
    MAIL_USERNAME = os.getenv('MAIL_USERNAME')
    MAIL_PASSWORD = os.getenv('MAIL_PASSWORD')
    MAIL_DEFAULT_SENDER = os.getenv('MAIL_DEFAULT_SENDER')