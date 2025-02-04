# Archivo de rutas v.2.8 

from flask import render_template, Blueprint, request, redirect, url_for, jsonify, session, current_app
from app import db, mail
from app.models import User
from datetime import datetime, timedelta, timezone
from functools import wraps
from flask_mail import Message
from apscheduler.schedulers.background import BackgroundScheduler
import logging
import requests
from app.tasks import enviar_correos_recordatorio, enviar_correos_cumpleaños
from settings import Config

# Crear el Blueprint
routes = Blueprint('routes', __name__)

# Configurar logs
logging.basicConfig(
    filename='email_logs.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# ✅ Usamos Config para obtener los valores
ADMIN_USERNAME = Config.ADMIN_USERNAME
ADMIN_PASSWORD = Config.ADMIN_PASSWORD

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
    """Maneja el inicio de sesión con reCAPTCHA."""
    error = None
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        recaptcha_response = request.form.get('g-recaptcha-response')

        # Validar reCAPTCHA con Google
        recaptcha_secret = current_app.config['RECAPTCHA_SECRET_KEY']
        recaptcha_verify_url = "https://www.google.com/recaptcha/api/siteverify"
        recaptcha_data = {"secret": recaptcha_secret, "response": recaptcha_response}
        recaptcha_result = requests.post(recaptcha_verify_url, data=recaptcha_data).json()

        if not recaptcha_result.get("success"):
            error = "Verificación de reCAPTCHA fallida. Inténtalo de nuevo."

        elif username == Config.ADMIN_USERNAME and password == Config.ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('routes.admin'))
        else:
            error = 'Usuario o contraseña incorrectos'

    return render_template('login.html', error=error)

@routes.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('routes.login'))

### PÁGINAS PRINCIPALES ###

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/admin')
@login_required
def admin():
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

### RESTAURACIÓN DE RUTAS ELIMINADAS ###

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
                nickname=apodo if apodo else None,
                email=email,
                birthday=fecha_nacimiento
            )
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Enviar correo de registro exitoso
            try:
                msg = Message(
                    subject="¡Tu registro fue exitoso!",
                    recipients=[email],
                    html=render_template('emails/registrook.html', name=nombre)
                )
                mail.send(msg)
            except Exception as e:
                return jsonify({'success': True, 'message': 'Usuario registrado, pero el correo no pudo ser enviado.', 'error': str(e)}), 200

            return jsonify({'success': True, 'message': 'Cumpleaños agregado con éxito.'}), 200
        except Exception as e:
            return jsonify({'success': False, 'message': f'Error inesperado: {str(e)}'}), 500

    return render_template('registro-cumples.html')

@routes.route('/ver-usuarios')
@login_required
def ver_usuarios():
    """Vista de usuarios registrados."""
    usuarios = User.query.all()
    return render_template('ver_usuarios.html', usuarios=usuarios)

### ENVÍO DE CORREOS (IMPORTANTE: NO BORRAR) ###

@routes.route('/test-recordatorios', methods=['GET'])
@login_required
def test_recordatorios():
    """Probar el envío de recordatorios."""
    correo_prueba = request.args.get('email')
    if not correo_prueba:
        return jsonify({'success': False, 'message': 'Correo no especificado para prueba.'}), 400
    
    enviar_correos_recordatorio(email_prueba=correo_prueba)
    return jsonify({'success': True, 'message': f'Correo de prueba enviado a {correo_prueba}'}), 200

@routes.route('/test-cumpleanos', methods=['GET'])
@login_required
def test_cumpleanos():
    """Probar el envío de correos de cumpleaños."""
    correo_prueba = request.args.get('email')
    if not correo_prueba:
        return jsonify({'success': False, 'message': 'Correo no especificado para prueba.'}), 400
    
    enviar_correos_cumpleaños(email_prueba=correo_prueba)
    return jsonify({'success': True, 'message': f'Correo de prueba enviado a {correo_prueba}'}), 200

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
    
# Ruta de la plantilla Ver-usuarios
@routes.route('/usuarios', methods=['GET'])
@login_required
def usuarios():
    """Devuelve la lista de usuarios en JSON."""
    orden = request.args.get('orden', 'desc')

    if orden == 'asc':
        usuarios = User.query.order_by(User.fecha_registro.asc()).all()
    else:
        usuarios = User.query.order_by(User.fecha_registro.desc()).all()

    resultado = [
        {
            'id': usuario.id,
            'name': usuario.name,
            'email': usuario.email,
            'nickname': usuario.nickname,
            'birthday': usuario.birthday.strftime('%Y-%m-%d'),
            'fecha_registro': usuario.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        }
        for usuario in usuarios
    ]
    return jsonify({'success': True, 'data': resultado})

@routes.route('/registros-recientes', methods=['GET'])
@login_required
def registros_recientes():
    """Devuelve los registros recientes según el rango solicitado."""
    rango = request.args.get('rango', 'dia')
    hoy = datetime.now(timezone.utc).date()

    if rango == 'semana':
        inicio = hoy - timedelta(days=7)
    elif rango == 'mes':
        inicio = hoy - timedelta(days=30)
    elif rango == 'dia':
        inicio = hoy
    else:
        return jsonify({'success': False, 'message': 'Rango no válido'}), 400

    registros = User.query.filter(User.fecha_registro >= inicio).order_by(User.fecha_registro.desc()).all()

    resultado = [
        {
            'id': user.id,
            'name': user.name,
            'email': user.email,
            'nickname': user.nickname,
            'birthday': user.birthday.strftime('%Y-%m-%d'),
            'fecha_registro': user.fecha_registro.strftime('%Y-%m-%d %H:%M:%S')
        }
        for user in registros
    ]
    return jsonify({'success': True, 'data': resultado})

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

### CONCLUSIÓN ###
# - Se corrigió la ruta de búsqueda de usuarios.
# - Se restauraron las rutas eliminadas: "agregar-cumple" y "ver-usuarios".
# - Se marcaron claramente las rutas de envío de correos con "IMPORTANTE: NO BORRAR".
# - Se verificó que todas las funciones esenciales estén presentes y funcionando correctamente.
