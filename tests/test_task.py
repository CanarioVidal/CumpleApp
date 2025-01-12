# Prueba de tareas programadas v1.2
from app import create_app
from app.email_utils import enviar_correos_recordatorio, enviar_correos_cumpleaños

# Crear la app y establecer el contexto
app = create_app()

with app.app_context():
    print("Enviando recordatorios...")
    enviar_correos_recordatorio()

    print("\nEnviando saludos...")
    enviar_correos_cumpleaños()
