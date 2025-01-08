from flask import render_template, Blueprint, request, redirect, url_for, jsonify, session
from app import db
from app.models import User
from datetime import datetime
from functools import wraps

# Crear el Blueprint
routes = Blueprint('routes', __name__)

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
    return render_template('admin.html', logout_url=url_for('routes.logout'))

# Ruta para agregar usuarios con soporte para GET y POST
@routes.route('/agregar-cumple', methods=['GET', 'POST'])
def agregar_usuario():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form.get('name')
            email = request.form.get('email')
            fecha_nacimiento = request.form.get('birthday')
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()

            # Crear nuevo usuario
            nuevo_usuario = User(name=nombre, email=email, birthday=fecha_nacimiento)
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Responder a AJAX con éxito
            return jsonify({'success': True}), 200
        except Exception as e:
            # Responder a AJAX con error
            return jsonify({'success': False, 'error': str(e)}), 400
    
    # Si es GET, renderizar el formulario
    return render_template('registro-cumples.html')

# Vista temporal de usuarios
@routes.route('/ver-usuarios')
@login_required
def ver_usuarios():
    usuarios = User.query.all()
    return render_template('ver_usuarios.html', usuarios=usuarios)
