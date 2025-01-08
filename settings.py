import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta_super_segura')

    # Configuración FIJA para asegurar la ruta absoluta
    SQLALCHEMY_DATABASE_URI = 'sqlite:///E:/cumpleapp/instance/cumpleapp.db'

    SQLALCHEMY_TRACK_MODIFICATIONS = False
