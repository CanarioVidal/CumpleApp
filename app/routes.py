from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>¡Página principal funcionando!</h1>"

@app.route('/admin')
def admin():
    return "<h1>¡Admin funcionando!</h1>"