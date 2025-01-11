from flask import Flask
from flask_mail import Mail, Message
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

app = Flask(__name__)

# Configuración del correo electrónico
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT'))
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS') == 'True'
app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL') == 'True'
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')

mail = Mail(app)

with app.app_context():
    try:
        msg = Message("Prueba de CumpleApp", recipients=["alejandro.caillava@gmail.com"])
        msg.body = "¡Este es un correo de prueba desde CumpleApp!"
        mail.send(msg)
        print("Correo enviado correctamente.")
    except Exception as e:
        print(f"Error al enviar correo: {str(e)}")
