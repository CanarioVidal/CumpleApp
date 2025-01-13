# Archivo de rutas v.1.3

from flask import render_template, Blueprint, request, redirect, url_for, jsonify, session
from app import db, mail
from app.models import User
from datetime import datetime, timedelta
from functools import wraps
from flask_mail import Message
from app import create_app
from flask_mail import Mail
from apscheduler.schedulers.background import BackgroundScheduler
import logging
from flask import current_app

# Crear el Blueprint
routes = Blueprint('routes', __name__)

# Configurar logs
logging.basicConfig(filename='email_logs.log', level=logging.INFO,
                    format='%(asctime)s - %(levelname)s - %(message)s')

# Simular credenciales de administrador (se puede mejorar luego)
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "1234"

# Decorador para proteger rutas
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('routes.login'))
        return f(*args, **kwargs)
    return decorated_function

# Ruta para iniciar sesión
@routes.route('/login', methods=['GET', 'POST'])
def login():
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

# Ruta para cerrar sesión
@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

@routes.route('/')
def home():
    return render_template('index.html')

# Ruta protegida para admin
@routes.route('/admin')
@login_required
def admin():
    hoy = datetime.today()
    cumpleanios_hoy = User.query.filter(
        db.extract('month', User.birthday) == hoy.month,
        db.extract('day', User.birthday) == hoy.day
    ).all()
    return render_template('admin.html', logout_url=url_for('routes.logout'), cumpleanios_hoy=cumpleanios_hoy)

# Ruta para obtener los cumpleaños del día en formato JSON
@routes.route('/cumpleanios-hoy', methods=['GET'])
@login_required
def cumpleanios_hoy():
    hoy = datetime.today()
    cumpleanios_hoy = User.query.filter(
        db.extract('month', User.birthday) == hoy.month,
        db.extract('day', User.birthday) == hoy.day
    ).all()
    
    # Convertir los resultados a JSON
    resultados = [
        {
            "name": usuario.name,
            "nickname": usuario.nickname or "N/A",
            "email": usuario.email,
            "redeemed": usuario.redeemed
        }
        for usuario in cumpleanios_hoy
    ]
    return jsonify(resultados)

# Ruta para agregar usuarios con soporte para GET y POST
@routes.route('/agregar-cumple', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form.get('name')
            apodo = request.form.get('nickname')
            email = request.form.get('email')
            fecha_nacimiento = request.form.get('birthday')

            # Validar campos obligatorios
            if not nombre or not email or not fecha_nacimiento:
                return jsonify({'success': False, 'message': 'Todos los campos obligatorios deben estar completos.'}), 400

            # Validar formato de fecha
            try:
                fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()
            except ValueError:
                return jsonify({'success': False, 'message': 'Formato de fecha no válido.'}), 400

            # Validar que el usuario sea mayor de 18 años
            hoy = datetime.today().date()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            if edad < 18:
                return jsonify({'success': False, 'message': 'El usuario debe ser mayor de 18 años.'}), 400

            # Validar que el correo no esté duplicado
            if User.query.filter_by(email=email).first():
                return jsonify({'success': False, 'message': 'El correo electrónico ya está registrado.'}), 400

            # Crear nuevo usuario
            nuevo_usuario = User(
                name=nombre,
                nickname=apodo if apodo else None,  # Guardar apodo solo si fue proporcionado
                email=email,
                birthday=fecha_nacimiento
            )
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Responder a AJAX con éxito
            return jsonify({'success': True, 'message': 'Cumpleaños agregado con éxito.'}), 200
        except Exception as e:
            # Responder a AJAX con error genérico
            return jsonify({'success': False, 'message': f'Error inesperado: {str(e)}'}), 500

    # Si es GET, renderizar el formulario
    return render_template('registro-cumples.html')

# Vista temporal de usuarios
@routes.route('/ver-usuarios')
@login_required
def ver_usuarios():
    usuarios = User.query.all()
    return render_template('ver_usuarios.html', usuarios=usuarios)

# Ruta para borrar un usuario por ID
@routes.route('/borrar-usuario/<int:id>', methods=['DELETE'])
@login_required
def borrar_usuario(id):
    try:
        usuario = User.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Ruta para borrar usuarios por batch
@routes.route('/borrar-usuarios', methods=['POST'])
@login_required
def borrar_usuarios():
    try:
        data = request.get_json()  # Recibe JSON
        ids = data.get('ids', [])  # Lista de IDs a borrar

        if not ids:
            return jsonify({'success': False, 'error': 'No se proporcionaron IDs para borrar.'}), 400

        # Borrar los usuarios con los IDs especificados
        User.query.filter(User.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'success': True}), 200
    except Exception as e:
        return jsonify({'success': False, 'error': f'Error al borrar usuarios: {str(e)}'}), 500

# Funciones para envío automático de correos
def enviar_correo(email, subject, body):
    try:
        msg = Message(subject, recipients=[email])
        msg.body = body
        with current_app.app_context():
            mail.send(msg)
        logging.info(f"Correo enviado a {email}")
    except Exception as e:
        logging.error(f"Error al enviar correo a {email}: {str(e)}")

def programar_correos():
    hoy = datetime.today().date()
    cumple_hoy = User.query.filter(
        db.extract('month', User.birthday) == hoy.month,
        db.extract('day', User.birthday) == hoy.day
    ).all()
    for usuario in cumple_hoy:
        saludo = usuario.nickname if usuario.nickname else usuario.name
        enviar_correo(usuario.email, "¡Feliz Cumpleaños!", f"Hola {saludo}, ¡Feliz cumpleaños! Ven a redimir tu obsequio.")

@routes.route('/tests/test-email', methods=['GET'])
@login_required
def test_email():
    try:
        # Crear el mensaje de correo
        msg = Message(
            subject="Correo de Prueba",
            recipients=["correo_destinatario@example.com"],  # Cambiar por un correo real
            body="Este es un correo de prueba enviado desde CumpleApp."
        )
        mail.send(msg)
        return jsonify({"success": True, "message": "Correo enviado exitosamente."}), 200
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 500
