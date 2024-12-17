from flask import render_template
from . import db

# Ruta principal
def home():
    return render_template('index.html')
