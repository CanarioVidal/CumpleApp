# Envío de correos v1.0
from flask_mail import Message
from app.models import User
from flask import current_app
from app import mail, db
from datetime import datetime, timedelta
import logging

# Configurar logs para correos
logging.basicConfig(
    filename='email_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def enviar_correo(email, subject, body):
    """
    Envía un correo electrónico utilizando Flask-Mail.
    :param email: Dirección del destinatario
    :param subject: Asunto del correo
    :param body: Cuerpo del correo
    """
    try:
        msg = Message(subject, recipients=[email])
        msg.body = body
        with current_app.app_context():
            mail.send(msg)
        logging.info(f"Correo enviado a {email} con asunto '{subject}'")
    except Exception as e:
        logging.error(f"Error al enviar correo a {email}: {str(e)}")

def enviar_correos_cumpleaños():
    """
    Envía correos electrónicos a los usuarios cuyo cumpleaños sea hoy.
    """
    hoy = datetime.today().date()
    cumple_hoy = User.query.filter(
        db.extract('month', User.birthday) == hoy.month,
        db.extract('day', User.birthday) == hoy.day
    ).all()

    if cumple_hoy:
        logging.info(f"Usuarios con cumpleaños hoy: {[u.email for u in cumple_hoy]}")
        for usuario in cumple_hoy:
            enviar_correo(
                usuario.email,
                "¡Feliz Cumpleaños!",
                f"Hola {usuario.name}, ¡Feliz cumpleaños! Ven a redimir tu obsequio."
            )
    else:
        logging.info("No hay cumpleaños para hoy.")

def enviar_correos_recordatorio():
    """
    Envía correos de recordatorio a usuarios con cumpleaños en los próximos 15 días.
    """
    hoy = datetime.today().date()
    recordatorio_inicio = datetime(hoy.year, hoy.month, 1).date()
    recordatorio_mitad = datetime(hoy.year, hoy.month, 16).date()

    if hoy == recordatorio_inicio or hoy == recordatorio_mitad:
        proximo_periodo = hoy + timedelta(days=15)
        recordatorio = User.query.filter(
            db.extract('month', User.birthday) == proximo_periodo.month,
            db.extract('day', User.birthday) == proximo_periodo.day
        ).all()

        if recordatorio:
            logging.info(f"Usuarios con cumpleaños próximos: {[u.email for u in recordatorio]}")
            for usuario in recordatorio:
                enviar_correo(
                    usuario.email,
                    "¡Tu cumpleaños se acerca!",
                    f"Hola {usuario.name}, faltan 15 días para tu cumpleaños."
                )
        else:
            logging.info("No hay cumpleaños próximos para recordatorio.")
    else:
        logging.info("No es fecha de recordatorio.")

def programar_correos():
    """
    Combina las funciones de correos de cumpleaños y recordatorios.
    """
    enviar_correos_cumpleaños()
    enviar_correos_recordatorio()
