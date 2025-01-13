# Iniciador de la app v.1.5
from app import create_app
from dotenv import load_dotenv, find_dotenv
import os
load_dotenv(find_dotenv())

# Por si necesitamos depurarlo nuevamente en el futuro
if __name__ == "__main__" and os.getenv("DEBUG", "False").lower() in ("true", "1", "yes"):
    print(f"MAIL_SERVER: {os.getenv('MAIL_SERVER')}")
    print(f"MAIL_PORT: {os.getenv('MAIL_PORT')}")
    print(f"MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
    print(f"MAIL_PASSWORD: {os.getenv('MAIL_PASSWORD')}")
    print(f"MAIL_DEFAULT_SENDER: {os.getenv('MAIL_DEFAULT_SENDER')}")

from settings import Config

try:
    Config.validate_email_config()
    print("Configuración de correo validada correctamente.")
except ValueError as e:
    print(f"Error en la validación de correo: {e}")
    exit(1)  # Detenemos la ejecución si faltan configuraciones críticas


app = create_app()

if __name__ == '__main__':
    app.run(debug=True)
