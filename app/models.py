from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)  # columna para id único de cada user en la app
    name = db.Column(db.String(50), nullable=False)  # columna para nombre
    nickname = db.Column(db.String(50), nullable=True)  # columna para apodo
    email = db.Column(db.String(120), unique=True, nullable=False)  # columna para email
    birthday = db.Column(db.Date, nullable=False)  # columna para cumpleaños
    redeemed = db.Column(db.Boolean, default=False)  # columna para registrar si obtuvo o no su regalo
