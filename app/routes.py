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
@routes.route('/admin', methods=['GET', 'POST'])
@login_required
def admin():
    if request.method == 'POST':
        try:
            # Obtener datos del formulario
            nombre = request.form.get('name')
            email = request.form.get('email')
            fecha_nacimiento = request.form.get('birthday')
            fecha_nacimiento = datetime.strptime(fecha_nacimiento, '%Y-%m-%d').date()

            # Validar que el usuario sea mayor de 18 años
            hoy = datetime.today().date()
            edad = hoy.year - fecha_nacimiento.year - ((hoy.month, hoy.day) < (fecha_nacimiento.month, fecha_nacimiento.day))
            if edad < 18:
                return jsonify({'success': False, 'error': 'Debe ser mayor de 18 años para registrarse.'}), 400

            # Crear nuevo usuario
            nuevo_usuario = User(name=nombre, email=email, birthday=fecha_nacimiento)
            db.session.add(nuevo_usuario)
            db.session.commit()

            # Responder a AJAX con éxito
            return jsonify({'success': True, 'message': 'Cumpleaños agregado con éxito.'}), 200
        except Exception as e:
            # Responder a AJAX con error específico
            return jsonify({'success': False, 'error': str(e)}), 400

    hoy = datetime.today()
    cumpleanios_hoy = User.query.filter(
        db.extract('month', User.birthday) == hoy.month,
        db.extract('day', User.birthday) == hoy.day
    ).all()
    return render_template('admin.html', logout_url=url_for('routes.logout'), cumpleanios_hoy=cumpleanios_hoy)

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

# Ruta para borrar múltiples usuarios
@routes.route('/borrar-usuarios', methods=['POST'])
@login_required
def borrar_usuarios():
    try:
        data = request.json
        ids = data.get('ids', [])
        User.query.filter(User.id.in_(ids)).delete(synchronize_session=False)
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Ruta para actualizar el estado de redención
@routes.route('/actualizar-redencion/<int:id>', methods=['POST'])
@login_required
def actualizar_redencion(id):
    data = request.json
    usuario = User.query.get_or_404(id)
    usuario.redeemed = data.get('redeemed', False)
    db.session.commit()
    return jsonify({'success': True})

# Ruta para buscar usuarios
@routes.route('/buscar-usuarios')
@login_required
def buscar_usuarios():
    query = request.args.get('q', '').strip()
    if query:
        usuarios = User.query.filter(
            (User.name.ilike(f"%{query}%")) | (User.email.ilike(f"%{query}%"))
        ).all()
    else:
        usuarios = []
    resultados = [{'id': u.id, 'name': u.name, 'email': u.email, 'birthday': u.birthday.strftime('%Y-%m-%d'), 'redeemed': u.redeemed} for u in usuarios]
    return jsonify(resultados)
