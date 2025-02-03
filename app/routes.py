# Archivo de rutas v.2.5 (Optimizado)

from flask import render_template, Blueprint, request, redirect, url_for, jsonify, session, current_app
from app import db, mail
from app.models import User
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask_mail import Message
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from app.tasks import enviar_correos_recordatorio, enviar_correos_cumpleaños

# Crear el Blueprint
routes = Blueprint('routes', __name__)

# Configurar logs
logging.basicConfig(
    filename='email_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# Simular credenciales de administrador (esto debería cambiarse en el futuro a un sistema seguro)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Decorador para proteger rutas de administración
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

### AUTENTICACIÓN ###

@routes.route('/login', methods=['GET', 'POST'])
def login():
    """Maneja el inicio de sesión del administrador."""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('routes.admin'))
        else:
            error = 'Usuario o contraseña incorrectos'
    return render_template('login.html', error=error)

@routes.route('/logout')
def logout():
    """Cierra la sesión del administrador."""
    session.clear()
    return redirect(url_for('routes.login'))

### PÁGINAS PRINCIPALES ###

@routes.route('/')
def home():
    """Página de inicio."""
    return render_template('index.html')

@routes.route('/admin')
@login_required
def admin():
    """Panel de administración."""
    hoy = datetime.today()
    cumpleanios_hoy = User.query.filter(
        db.extract('month', User.birthday) == hoy.month,
        db.extract('day', User.birthday) == hoy.day
    ).all()
    return render_template('admin.html', logout_url=url_for('routes.logout'), cumpleanios_hoy=cumpleanios_hoy)

### API: CONSULTAS DE USUARIOS ###

@routes.route('/cumpleanios-hoy', methods=['GET'])
@login_required
def cumpleanios_hoy():
    """Devuelve la lista de usuarios que cumplen años hoy en formato JSON."""
    hoy = datetime.today()
    cumpleanios = User.query.filter(
        db.extract('month', User.birthday) == hoy.month,
        db.extract('day', User.birthday) == hoy.day
    ).all()
    
    return jsonify([{
        "name": user.name,
        "nickname": user.nickname or "N/A",
        "email": user.email,
        "redeemed": user.redeemed
    } for user in cumpleanios])

@routes.route('/buscar-usuarios', methods=['GET'])
@login_required
def buscar_usuarios():
    """Busca usuarios por nombre, apodo o email."""
    query = request.args.get('q', '').strip()
    if not query:
        return jsonify([]), 400

    resultados = User.query.filter(
        (User.name.ilike(f'%{query}%')) |
        (User.nickname.ilike(f'%{query}%')) |
        (User.email.ilike(f'%{query}%'))
    ).all()

    return jsonify([{
        "name": user.name,
        "nickname": user.nickname or "N/A",
        "email": user.email,
        "birthday": user.birthday.strftime('%Y-%m-%d'),
        "redeemed": user.redeemed
    } for user in resultados])

### MANEJO DE USUARIOS ###

@routes.route('/agregar-cumple', methods=['GET', 'POST'])
def agregar_usuario():
    """Agrega un nuevo usuario y envía un correo de bienvenida."""
    if request.method == 'POST':
        try:
            data = request.form
            nombre = data.get('name')
            apodo = data.get('nickname')
            email = data.get('email')
            fecha_nacimiento = data.get('birthday')

            if not nombre or not email or not fecha_nacimiento:
                return jsonify({'success': False, 'message': 'Todos los campos obligatorios deben estar completos.'}), 400

            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            edad = (datetime.today().date() - fecha_nacimiento).days // 365
            if edad < 18:
                return jsonify({'success': False, 'message': 'El usuario debe ser mayor de 18 años.'}), 400

            if User.query.filter_by(email=email).first():
                return jsonify({'success': False, 'message': 'El correo electrónico ya está registrado.'}), 400

            nuevo_usuario = User(name=nombre, nickname=apodo, email=email, birthday=fecha_nacimiento)
            db.session.add(nuevo_usuario)
            db.session.commit()

            try:
                msg = Message(
                    subject="¡Tu registro fue exitoso!",
                    recipients=[email],
                    html=render_template('emails/registrook.html', name=nombre)
                )
                mail.send(msg)
            except Exception as e:
                logging.error(f"Error al enviar correo: {e}")

            return jsonify({'success': True, 'message': 'Cumpleaños agregado con éxito.'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error inesperado: {str(e)}'}), 500

    return render_template('registro-cumples.html')

### ENVÍO DE CORREOS ###

def enviar_correo(email, subject, body):
    """Envía un correo."""
    try:
        msg = Message(subject, recipients=[email])
        msg.body = body
        with current_app.app_context():
            mail.send(msg)
        logging.info(f"Correo enviado a {email}")
    except Exception as e:
        logging.error(f"Error al enviar correo a {email}: {str(e)}")

@routes.route('/tests/test-email', methods=['GET'])
@login_required
def test_email():
    """Prueba el envío de correos."""
    try:
        msg = Message(
            subject="Correo de Prueba",
            recipients=["correo_destinatario@example.com"],
            body="Este es un correo de prueba enviado desde CumpleApp."
        )
        mail.send(msg)
        return jsonify({"success": True, "message": "Correo enviado exitosamente."}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500

### TAREAS PROGRAMADAS ###

@routes.route('/tests/probar-recordatorios', methods=['GET'])
@login_required
def probar_recordatorios():
    """Prueba el envío de recordatorios."""
    try:
        enviar_correos_recordatorio()
        return jsonify({'success': True, 'message': 'Prueba de recordatorios realizada con éxito.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500

@routes.route('/tests/probar-cumpleaños', methods=['GET'])
@login_required
def probar_cumpleaños():
    """Prueba el envío de correos de cumpleaños."""
    try:
        enviar_correos_cumpleaños()
        return jsonify({'success': True, 'message': 'Prueba de cumpleaños realizada con éxito.'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)}), 500
