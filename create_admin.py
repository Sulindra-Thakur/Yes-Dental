from app import app
from models import db, User
from werkzeug.security import generate_password_hash

with app.app_context():

    # (optional) check if admin already exists
    existing_admin = User.query.filter_by(email="admin@gmail.com").first()

    if existing_admin:
        print("Admin already exists!")
    else:
        admin = User(
            email="admin@gmail.com",
            name="Admin",
            password=generate_password_hash("admin123"),
            is_admin=True
        )

        db.session.add(admin)
        db.session.commit()

        print("Admin created successfully!")