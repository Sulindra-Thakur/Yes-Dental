from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin

db = SQLAlchemy()

# ---------------- USER ----------------
class User(db.Model, UserMixin):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    reset_token = db.Column(db.String(255), nullable=True)
    reset_token_used = db.Column(db.Boolean, default=False)

    appointments = db.relationship('Appointment', backref='user', lazy=True)


# ---------------- APPOINTMENT ----------------
class Appointment(db.Model):
    __tablename__ = 'appointments'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    fullname = db.Column(db.String(100), nullable=False)
    phone = db.Column(db.String(13), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    address = db.Column(db.Text)

    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)

    treatment = db.Column(db.String(100), nullable=False)
    notes = db.Column(db.Text)

    service_type = db.Column(db.String(200))
    specialist = db.Column(db.String(200))

    status = db.Column(db.String(20), default='pending')  # FIXED (lowercase consistent)

    is_deleted = db.Column(db.Boolean, default=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)


# ---------------- REVIEW / CONTACT MESSAGE ----------------

class Review(db.Model):
    __tablename__ = 'reviews'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(150), nullable=False)

    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)

    created_at = db.Column(db.DateTime, default=datetime.utcnow)

