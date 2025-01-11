# Define las tareas programadas con APScheduler v.1.0
from apscheduler.schedulers.background import BackgroundScheduler
from app.email_utils import programar_correos  # Importa la lógica de envío de correos
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

        # Programar las tareas
        scheduler.add_job(
            programar_correos,
            'cron',
            hour=11,  # Corre todos los días a las 11 AM
            id='correo_diario',
            replace_existing=True
        )
        scheduler.add_job(
            programar_correos,
            'cron',
            day=1,
            hour=11,  # Corre el 1ro de cada mes a las 11 AM
            id='correo_1ro_mes',
            replace_existing=True
        )
        scheduler.add_job(
            programar_correos,
            'cron',
            day=16,
            hour=11,  # Corre el 16 de cada mes a las 11 AM
            id='correo_16_mes',
            replace_existing=True
        )

        # Iniciar el scheduler
        scheduler.start()
        logging.info('Tareas programadas iniciadas correctamente.')
    except Exception as e:
        logging.error(f'Error al iniciar tareas programadas: {str(e)}')
