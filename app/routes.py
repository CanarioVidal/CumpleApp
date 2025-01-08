from flask import render_template, Blueprint

# Crear el Blueprint
routes = Blueprint('routes', __name__)

@routes.route('/')
def home():
    return render_template('index.html')

@routes.route('/admin')
def admin():
    return render_template('admin.html')
