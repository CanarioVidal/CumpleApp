from app import db

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    birthday = db.Column(db.Date, nullable=False)
    redeemed = db.Column(db.Boolean, default=False)
