# Define las tareas programadas con APScheduler v.1.7
from apscheduler.schedulers.background import BackgroundScheduler
from app.email_utils import enviar_correos_recordatorio, enviar_correos_cumpleaños
import logging

# Configurar logs para tareas
logging.basicConfig(
    filename='email_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def iniciar_tareas(app):
    """Inicializa las tareas programadas con APScheduler."""
    try:
        scheduler = BackgroundScheduler()

        def tarea_recordatorio():
            with app.app_context():
                enviar_correos_recordatorio()

        def tarea_cumpleaños():
            with app.app_context():
                enviar_correos_cumpleaños()

        # Programar recordatorios de cumpleaños (1 semana antes)
        scheduler.add_job(
            tarea_recordatorio,
            'cron',
            hour=11, minute=00,  # Cambia según el horario que prefieras
            id='recordatorios_diarios',
            replace_existing=True
        )

        # Programar saludos de cumpleaños (en el día)
        scheduler.add_job(
            tarea_cumpleaños,
            'cron',
            hour=11, minute=00,  # Cambia según el horario que prefieras
            id='saludos_diarios',
            replace_existing=True
        )

        # Iniciar el scheduler
        scheduler.start()

        # Imprimir próxima ejecución de las tareas programadas
        for job in scheduler.get_jobs():
            logging.info(f"Tarea programada: {job.id} - Siguiente ejecución: {job.next_run_time}")
        
        logging.info('Tareas programadas iniciadas correctamente.')
    except Exception as e:
        logging.error(f'Error al iniciar tareas programadas: {str(e)}')
