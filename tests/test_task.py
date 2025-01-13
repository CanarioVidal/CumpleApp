# Prueba de tareas programadas v1.3
import os
import sys
from dotenv import load_dotenv

# Asegurarse de que el directorio raíz del proyecto esté en sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Cargar el archivo .env
load_dotenv()

# Imprimir valores para verificar
print(f"MAIL_SERVER: {os.getenv('MAIL_SERVER')}")
print(f"MAIL_USERNAME: {os.getenv('MAIL_USERNAME')}")
print(f"MAIL_PASSWORD: {os.getenv('MAIL_PASSWORD')}")
print(f"MAIL_DEFAULT_SENDER: {os.getenv('MAIL_DEFAULT_SENDER')}")


from app import create_app
from app.email_utils import enviar_correos_recordatorio, enviar_correos_cumpleaños

# Crear la app y establecer el contexto
app = create_app()

with app.app_context():
    print("Enviando recordatorios...")
    enviar_correos_recordatorio()

    print("\nEnviando saludos...")
    enviar_correos_cumpleaños()
