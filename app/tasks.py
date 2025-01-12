# Define las tareas programadas con APScheduler v.1.1
from apscheduler.schedulers.background import BackgroundScheduler
from app.email_utils import enviar_recordatorios, enviar_saludos_cumpleanios  # Nuevas funciones para correos
import logging

# Configurar logs para tareas
logging.basicConfig(
    filename='email_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def iniciar_tareas():
    """Inicializa las tareas programadas con APScheduler."""
    try:
        scheduler = BackgroundScheduler()

        # Programar recordatorios de cumpleaños (1 semana antes)
        scheduler.add_job(
            enviar_recordatorios,
            'cron',
            hour=11,  # Corre todos los días a las 11 AM
            id='recordatorios_diarios',
            replace_existing=True
        )

        # Programar saludos de cumpleaños (en el día)
        scheduler.add_job(
            enviar_saludos_cumpleanios,
            'cron',
            hour=12,  # Corre todos los días a las 12 PM
            id='saludos_diarios',
            replace_existing=True
        )

        # Iniciar el scheduler
        scheduler.start()
        logging.info('Tareas programadas iniciadas correctamente.')
    except Exception as e:
        logging.error(f'Error al iniciar tareas programadas: {str(e)}')
