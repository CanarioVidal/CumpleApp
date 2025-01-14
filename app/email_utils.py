# Envío de correos v1.5.1
from flask_mail import Message
from flask import current_app, render_template
from app import mail, db
from app.models import User
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
        msg = Message(
            subject=subject,
            recipients=[email],
            sender=current_app.config['MAIL_DEFAULT_SENDER']  # Especificar remitente explícitamente
        )
        msg.body = body
        with current_app.app_context():
            mail.send(msg)
        logging.info(f"Correo enviado a {email} con asunto '{subject}'")
    except Exception as e:
        logging.error(f"Error al enviar correo a {email}: {str(e)}")

def enviar_correos_recordatorio(email_prueba=None):
    """
    Envía correos recordatorios a los usuarios cuyo cumpleaños es dentro de 7 días.
    También soporta el envío de un correo de prueba.
    """
    if email_prueba:
        # Enviar un correo de prueba de recordatorio
        print(f"Enviando correo de prueba de recordatorio a: {email_prueba}")
        try:
            msg = Message(
                subject="Recordatorio Especial",
                recipients=[email_prueba],
                sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Especificar remitente explícitamente
                html=render_template('emails/recordatorio.html', name="Usuario de Prueba")
            )
            mail.send(msg)
            print(f"Correo de prueba enviado correctamente a: {email_prueba}")
            return True
        except Exception as e:
            print(f"Error al enviar correo de prueba: {str(e)}")
            return False

    # Lógica para enviar recordatorios a usuarios con cumpleaños en 7 días
    hoy = datetime.now().date()
    objetivo = hoy + timedelta(days=7)

    try:
        # Consultar usuarios cuyo cumpleaños está en 7 días
        usuarios = User.query.filter(
            db.extract('month', User.birthday) == objetivo.month,
            db.extract('day', User.birthday) == objetivo.day
        ).all()

        if not usuarios:
            current_app.logger.info("No hay usuarios con cumpleaños en 7 días.")
            return

        for usuario in usuarios:
            try:
                msg = Message(
                    subject="¡Tu cumpleaños está cerca!",
                    recipients=[usuario.email],
                    sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Especificar remitente explícitamente
                    html=render_template('emails/recordatorio.html', name=usuario.name)
                )
                mail.send(msg)
                print(f"Recordatorio enviado a: {usuario.email}")
                current_app.logger.info(f"Recordatorio enviado a: {usuario.email}")
            except Exception as e:
                print(f"Error al enviar recordatorio a {usuario.email}: {str(e)}")
                current_app.logger.error(f"Error al enviar recordatorio a {usuario.email}: {str(e)}")

    except Exception as general_error:
        print(f"Error general en enviar_correos_recordatorio: {str(general_error)}")
        current_app.logger.error(f"Error general en enviar_correos_recordatorio: {str(general_error)}")

def enviar_correos_cumpleaños(email_prueba=None):
    """
    Envía correos de cumpleaños a los usuarios cuyo cumpleaños es hoy.
    También soporta el envío de un correo de prueba.
    """
    if email_prueba:
        # Enviar un correo de prueba de cumpleaños
        print(f"Enviando correo de prueba de cumpleaños a: {email_prueba}")
        try:
            msg = Message(
                subject="¡Feliz Cumpleaños!",
                recipients=[email_prueba],
                sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Especificar remitente explícitamente
                html=render_template('emails/saludo.html', name="Usuario de Prueba")
            )
            mail.send(msg)
            print(f"Correo de prueba enviado correctamente a: {email_prueba}")
            return True
        except Exception as e:
            print(f"Error al enviar correo de prueba: {str(e)}")
            return False

    # Lógica para enviar correos de cumpleaños a los usuarios cuyo cumpleaños es hoy
    hoy = datetime.now().date()

    try:
        # Consultar usuarios cuyo cumpleaños es hoy
        usuarios = User.query.filter(
            db.extract('month', User.birthday) == hoy.month,
            db.extract('day', User.birthday) == hoy.day
        ).all()

        if not usuarios:
            current_app.logger.info("No hay usuarios con cumpleaños hoy.")
            return

        for usuario in usuarios:
            try:
                msg = Message(
                    subject="¡Feliz Cumpleaños!",
                    recipients=[usuario.email],
                    sender=current_app.config['MAIL_DEFAULT_SENDER'],  # Especificar remitente explícitamente
                    html=render_template('emails/saludo.html', name=usuario.name)
                )
                mail.send(msg)
                print(f"Correo de cumpleaños enviado a: {usuario.email}")
                current_app.logger.info(f"Correo de cumpleaños enviado a: {usuario.email}")
            except Exception as e:
                print(f"Error al enviar correo de cumpleaños a {usuario.email}: {str(e)}")
                current_app.logger.error(f"Error al enviar correo de cumpleaños a {usuario.email}: {str(e)}")

    except Exception as general_error:
        print(f"Error general en enviar_correos_cumpleaños: {str(general_error)}")
        current_app.logger.error(f"Error general en enviar_correos_cumpleaños: {str(general_error)}")
