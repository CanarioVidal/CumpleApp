import os

class Config:
    # Clave secreta para proteger formularios y sesiones
    SECRET_KEY = os.getenv('SECRET_KEY', 'mi_clave_secreta_super_segura')

    # Configuración de la base de datos (por defecto usa SQLite)
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI', 'sqlite:///cumpleapp.db')

    # Desactiva el seguimiento de modificaciones para mejorar el rendimiento
    SQLALCHEMY_TRACK_MODIFICATIONS = False
