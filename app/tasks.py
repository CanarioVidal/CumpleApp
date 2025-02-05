# Define las tareas programadas con APScheduler v.1.8 (Ajustado para producción time zone arreglado)
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.jobstores.base import ConflictingIdError
from pytz import timezone
from app.email_utils import enviar_correos_recordatorio, enviar_correos_cumpleaños
import logging

# Configurar logs para tareas
logging.basicConfig(
    filename='email_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Definir la zona horaria de Uruguay (-03:00)
TZ_URUGUAY = timezone('America/Montevideo')

def iniciar_tareas(app):
    """Inicializa las tareas programadas con APScheduler en la zona horaria correcta."""
    try:
        # Configurar el scheduler con la zona horaria correcta
        scheduler = BackgroundScheduler(timezone=TZ_URUGUAY)

        def tarea_recordatorio():
            """Ejecuta la función de envío de recordatorios en el contexto de Flask."""
            with app.app_context():
                enviar_correos_recordatorio()

        def tarea_cumpleaños():
            """Ejecuta la función de envío de saludos en el contexto de Flask."""
            with app.app_context():
                enviar_correos_cumpleaños()

        # Verificar si las tareas ya están programadas antes de agregarlas
        jobs = {job.id for job in scheduler.get_jobs()}

        if 'recordatorios_diarios' not in jobs:
            scheduler.add_job(
                tarea_recordatorio,
                'cron',
                hour=10, minute=00,  # Se ejecuta a las 10:00 AM (-03:00) se puede modificar para pruebas
                id='recordatorios_diarios',
                replace_existing=True
            )

        if 'saludos_diarios' not in jobs:
            scheduler.add_job(
                tarea_cumpleaños,
                'cron',
                hour=10, minute=00,  # Se ejecuta a las 10:00 AM (-03:00) se puede modificar para pruebas
                id='saludos_diarios',
                replace_existing=True
            )

        # Iniciar el scheduler solo si no está ya en ejecución
        if not scheduler.running:
            scheduler.start()

        # Imprimir próximas ejecuciones en los logs
        for job in scheduler.get_jobs():
            logging.info(f"Tarea programada: {job.id} - Siguiente ejecución: {job.next_run_time}")

        logging.info('Tareas programadas iniciadas correctamente.')

    except ConflictingIdError as e:
        logging.warning(f'Intento de duplicar tareas programadas: {str(e)}')

    except Exception as e:
        logging.error(f'Error al iniciar tareas programadas: {str(e)}')
