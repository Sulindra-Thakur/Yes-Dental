# from flask import Flask, render_template, request, redirect, url_for, flash
# from flask_sqlalchemy import SQLAlchemy
# from flask_login import LoginManager, login_user, logout_user, login_required, current_user
# from werkzeug.security import generate_password_hash, check_password_hash
# from functools import wraps
# from datetime import datetime
# from werkzeug.utils import secure_filename

# from flask_mail import Mail, Message
# from itsdangerous import URLSafeTimedSerializer

# from dotenv import load_dotenv
# import os
# import sys
# load_dotenv()

# # Import models
# from models import db, User, Appointment, Review



# app = Flask(__name__)

# app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'my-dev-secret-key')

# app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
# app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
# app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

# serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])


# MYSQL_USER = os.getenv("MYSQL_USER")
# MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
# MYSQL_HOST = os.getenv("MYSQL_HOST")
# MYSQL_PORT = os.getenv("MYSQL_PORT", "3307")
# MYSQL_DB = os.getenv("MYSQL_DB")
# app.config['SQLALCHEMY_DATABASE_URI'] = (
#     f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
# )
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# from sqlalchemy import create_engine

# engine = create_engine(
#     app.config['SQLALCHEMY_DATABASE_URI'],
#     pool_pre_ping=True,
#     pool_recycle=280,
#     pool_size=5,
#     max_overflow=10
# )

# # ================= FOLDERS =================
# UPLOAD_IMAGE_FOLDER = 'static/images'
# UPLOAD_VIDEO_FOLDER = 'static/videos'

# app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
# app.config['UPLOAD_VIDEO_FOLDER'] = UPLOAD_VIDEO_FOLDER

# # ================= ALLOWED FILES =================
# ALLOWED_IMAGE = {'png', 'jpg', 'jpeg'}
# ALLOWED_VIDEO = {'mp4', 'mov', 'avi'}

# # ---------------- LOGIN MANAGER ----------------
# login_manager = LoginManager(app)
# login_manager.login_view = 'login'
# login_manager.login_message = "Please log in to access this page."


# @login_manager.user_loader
# def load_user(user_id):
#     return User.query.get(int(user_id))


# # ---------------- DB INIT ----------------
# try:
#     print("Connecting to MySQL...")
#     db.init_app(app)
#     with app.app_context():
#         db.create_all()
#     print("Database connected successfully!")
# except Exception as e:
#     print("CRITICAL ERROR: Database connection failed")
#     print(e)


# # ---------------- ADMIN DECORATOR ----------------
# def admin_required(f):
#     @wraps(f)
#     def wrapper(*args, **kwargs):
#         if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
#             flash("Admin access required", "danger")
#             return redirect(url_for("home"))
#         return f(*args, **kwargs)
#     return wrapper


# # ---------------- HELPER ----------------
# def allowed_file(filename, allowed_set):
#     return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set


# # ---------------- PUBLIC ROUTES ----------------
# @app.route('/')
# def home():
#     return render_template('pages.html')


# @app.route('/services')
# def services():
#     return render_template('services.html')


# @app.route('/about')
# def about():
#     return render_template('about.html')


# @app.route('/team')
# def team():
#     return render_template('team.html')


# @app.route('/contact', methods=['GET'])
# def contact():
#     return render_template('contact.html')


# # ---------------- BOOKING ----------------
# @app.route('/booking')
# def booking_page():
#     return render_template('booking.html')


# @app.route('/submit-booking', methods=['POST'])
# def submit_booking():
#     try:
#         appointment = Appointment(
#             user_id=current_user.id if current_user.is_authenticated else None,
#             fullname=request.form.get('fullname'),
#             phone=request.form.get('phone'),
#             email=request.form.get('email'),
#             address=request.form.get('address'),
#             date=request.form.get('date'),
#             time=request.form.get('time'),
#             treatment=request.form.get('treatment'),
#             service_type = (request.form.get("service_type") or "").strip(),
#             specialist = (request.form.get("specialist") or "").strip(),
#             notes=request.form.get('notes'),
#             status='pending'
#         )

#         db.session.add(appointment)
#         db.session.commit()

#         flash("Appointment booked successfully!", "success")
#         return redirect(url_for('booking_page'))

#     except Exception as e:
#         db.session.rollback()
#         print("Booking Error:", e)
#         flash("Booking failed. Try again.", "danger")
#         return redirect(url_for('booking_page'))


# # ---------------- AUTH ----------------
# @app.route('/register', methods=['GET', 'POST'])
# def register():
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))

#     if request.method == 'POST':
#         email = request.form.get('email')
#         name = request.form.get('name')
#         password = request.form.get('password')

#         if User.query.filter_by(email=email).first():
#             flash("Email already exists", "danger")
#             return redirect(url_for('register'))

#         user = User(
#             email=email,
#             name=name,
#             password=generate_password_hash(password)
#         )

#         db.session.add(user)
#         db.session.commit()

#         flash("Registered successfully. Please login.", "success")
#         return redirect(url_for('login'))

#     return render_template('register.html')


# @app.route('/login', methods=['GET', 'POST'])
# def login():
#     if current_user.is_authenticated:
#         return redirect(url_for('dashboard'))

#     if request.method == 'POST':
#         email = request.form.get('email')
#         password = request.form.get('password')
#         remember = bool(request.form.get('remember'))

#         user = User.query.filter_by(email=email).first()

#         if not user or not check_password_hash(user.password, password):
#             flash("Invalid credentials", "danger")
#             return redirect(url_for('login'))

#         login_user(user, remember=remember)
#         return redirect(url_for('dashboard'))

#     return render_template('login.html')


# @app.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     flash("Logged out successfully", "info")
#     return redirect(url_for('home'))


# # ---------------- USER DASHBOARD ----------------
# @app.route('/dashboard')
# @login_required
# def dashboard():
#     if getattr(current_user, "is_admin", False):
#         return redirect(url_for("admin_dashboard"))

#     appointments = Appointment.query.filter_by(
#         user_id=current_user.id,
#         is_deleted=False
#     ).order_by(Appointment.id.desc()).all()
#     return render_template('dashboard.html', name=current_user.name, appointments=appointments)


# # ----------------- ADMIN DASHBOARD -----------------
# @app.route('/admin/dashboard')
# @login_required
# @admin_required
# def admin_dashboard():
#     appointments = Appointment.query.filter_by(
#         is_deleted=False
#     ).order_by(Appointment.id.desc()).all()

#     reviews = Review.query.order_by(Review.id.desc()).all()

#     return render_template(
#         'admin_dashboard.html',
#         appointments=appointments,
#         reviews=reviews
#     )


# # ----------------- CLIENT DETAILS ROUTE -----------------
# @app.route('/admin/client-details')
# @login_required
# @admin_required
# def client_details():
#     appointments = Appointment.query.filter_by(
#         is_deleted=False
#     ).order_by(Appointment.id.desc()).all()
    
#     target_id = request.args.get('select_id', type=int)
#     # MODIFICATION: URL parameters check for auto-opening logs section on redirect
#     show_logs = request.args.get('show_logs', 'false')
    
#     return render_template(
#         'client_details.html', 
#         appointments=appointments, 
#         target_id=target_id,
#         show_logs=show_logs
#     )


# # ----------------- MODIFICATION: CONNECT COMMIT PROGRESS NOTE TO BACKEND -----------------
# @app.route('/add_treatment_log/<int:appt_id>', methods=['POST'])
# @login_required
# @admin_required
# def add_treatment_log(appt_id):
#     appointment = Appointment.query.get_or_404(appt_id)
#     new_note = request.form.get('doctor_note', '').strip()
    
#     if not new_note:
#         flash("Clinical progress note cannot be empty!", "danger")
#         return redirect(url_for('client_details', select_id=appt_id))
        
#     # Format current dynamic timestamp [YYYY-MM-DD HH:MM:SS]
#     current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#     formatted_new_note = f"[{current_time}] {new_note}"
    
#     existing_notes = appointment.notes if appointment.notes else ""
    
#     # Clean string garbage filter updates if any
#     for s in ["Pending", "Confirmed", "Rejected", "Completed"]:
#         if existing_notes.endswith(s) and not existing_notes.endswith(f"||| {s}"):
#             existing_notes = existing_notes[:-len(s)].strip()
            
#     # Structural processing layer check
#     if existing_notes:
#         appointment.notes = f"{existing_notes} ||| {formatted_new_note}"
#     else:
#         appointment.notes = f"Original Client Note Placeholder ||| {formatted_new_note}"
        
#     try:
#         db.session.commit()
#         flash('Progress note committed and clinical dashboard synced successfully!', 'success')
#     except Exception as e:
#         db.session.rollback()
#         print("Treatment log error details:", e)
#         flash('Failed to save progress log context structural update.', 'danger')
        
#     # Send custom system query instructions: select_id & show_logs=true
#     return redirect(url_for('client_details', select_id=appt_id, show_logs='true'))


# @app.route('/admin/appointment/<int:appt_id>/update', methods=['POST'])
# @login_required
# @admin_required
# def update_appointment(appt_id):
#     appointment = Appointment.query.get_or_404(appt_id)
    
#     new_note = request.form.get('notes', '').strip()
#     status = request.form.get('status')
    
#     if status:
#         appointment.status = status.strip()
        
#     if new_note:
#         current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
#         formatted_new_note = f"[{current_time}] {new_note}"
        
#         existing_notes = appointment.notes if appointment.notes else ""
        
#         for s in ["Pending", "Confirmed", "Rejected", "Completed"]:
#             if existing_notes.endswith(s) and not existing_notes.endswith(f"||| {s}"):
#                 existing_notes = existing_notes[:-len(s)].strip()
        
#         if existing_notes:
#             appointment.notes = f"{existing_notes} ||| {formatted_new_note}"
#         else:
#             appointment.notes = formatted_new_note
            
#     db.session.commit()
#     flash('Patient profile updated successfully!', 'success')
    
#     return redirect(url_for('admin_dashboard', select_id=appt_id))


# # --- ROUTES FOR SOFT DELETE, PERMANENT DELETE, AND RESTORE ---
# @app.route('/admin/delete_appointment/<int:id>')
# @login_required
# @admin_required
# def delete_appointment(id):
#     appointment = Appointment.query.get_or_404(id)
#     appointment.is_deleted = True
#     db.session.commit()
    
#     flash("Appointment moved to trash (soft deleted).", "warning")
#     return redirect(url_for("admin_dashboard"))


# @app.route('/admin/permanently_delete/<int:id>')
# @login_required
# @admin_required
# def permanently_delete_appointment(id):
#     appointment = Appointment.query.get_or_404(id)
    
#     if not appointment.is_deleted:
#         flash("Cannot permanently delete an active appointment. Please delete it first.", "danger")
#         return redirect(url_for("admin_dashboard"))

#     db.session.delete(appointment)
#     db.session.commit()
    
#     flash("Appointment permanently deleted.", "danger")
#     return redirect(url_for("admin_dashboard"))


# @app.route('/admin/restore_appointment/<int:id>')
# @login_required
# @admin_required
# def restore_appointment(id):
#     appointment = Appointment.query.get_or_404(id)
    
#     if not appointment.is_deleted:
#         flash("This appointment is not in trash.", "warning")
#         return redirect(url_for("admin_dashboard"))

#     appointment.is_deleted = False
#     db.session.commit()
    
#     flash("Appointment restored successfully.", "success")
#     return redirect(url_for("admin_dashboard"))


# @app.route('/admin/trash')
# @login_required
# @admin_required
# def admin_trash():
#     appointments = Appointment.query.filter_by(is_deleted=True).order_by(Appointment.id.desc()).all()
#     return render_template('admin_trash.html', appointments=appointments)


# @app.route('/admin/reviews')
# @login_required
# @admin_required
# def admin_Reviews():
#     reviews = Review.query.order_by(Review.id.desc()).all()
#     return render_template('admin_Reviews.html', reviews=reviews)


# @app.route('/admin/settings', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def admin_settings():
#     admin = current_user

#     if request.method == 'POST':
#         action = request.form.get('action')

#         if action == 'change_email':
#             new_email = request.form.get('email')
#             existing_user = User.query.filter_by(email=new_email).first()

#             if existing_user and existing_user.id != admin.id:
#                 flash('Email already exists!', 'danger')
#             else:
#                 admin.email = new_email
#                 db.session.commit()
#                 flash('Email updated successfully!', 'success')

#         elif action == 'change_password':
#             current_password = request.form.get('current_password', '').strip()
#             new_password = request.form.get('new_password', '').strip()
#             confirm_password = request.form.get('confirm_password', '').strip()

#             if not current_password or not new_password or not confirm_password:
#                 flash('All fields are required!', 'danger')
#             elif not check_password_hash(admin.password, current_password):
#                 flash('Current password is incorrect!', 'danger')
#             elif new_password != confirm_password:
#                 flash('Passwords do not match!', 'danger')
#             else:
#                 admin.password = generate_password_hash(new_password)
#                 db.session.commit()
#                 flash('Password updated successfully!', 'success')

#     return render_template('admin_settings.html', admin=admin)


# @app.route('/treatment-history')
# @login_required
# def treatment_history():
#     appointments = Appointment.query.filter_by(user_id=current_user.id).all()
#     return render_template('treatment_history.html', appointments=appointments, name=current_user.name)


# @app.route('/my-profile', methods=['GET', 'POST'])
# @login_required
# def my_profile():
#     user = current_user

#     if request.method == 'POST':
#         new_name = request.form.get('name')
#         new_email = request.form.get('email')

#         existing_user = User.query.filter_by(email=new_email).first()
#         if existing_user and existing_user.id != user.id:
#             flash("Email already exists!", "danger")
#             return redirect(url_for('my_profile'))

#         user.name = new_name
#         user.email = new_email
#         db.session.commit()

#         flash("Profile updated successfully!", "success")
#         return redirect(url_for('my_profile'))

#     appointments = Appointment.query.filter_by(user_id=user.id).all()
#     total = len(appointments)
#     pending = len([a for a in appointments if a.status == 'pending'])
#     confirmed = len([a for a in appointments if a.status == 'confirmed'])
#     recent_appointments = appointments[-3:][::-1]

#     return render_template(
#         'my_profile.html',
#         total=total,
#         pending=pending,
#         confirmed=confirmed,
#         recent_appointments=recent_appointments,
#         user=user
#     )


# @app.route('/profile', methods=['GET', 'POST'])
# @login_required
# def edit_profile():
#     user = current_user

#     if request.method == 'POST':
#         action = request.form.get('action')

#         if action == 'update_user':
#             new_name = request.form.get('name')
#             new_email = request.form.get('email')

#             existing = User.query.filter_by(email=new_email).first()
#             if existing and existing.id != user.id:
#                 flash("Email already exists!", "danger")
#                 return redirect(url_for('edit_profile'))

#             user.name = new_name
#             user.email = new_email
#             db.session.commit()
#             flash("Profile updated successfully!", "success")
#             return redirect(url_for('edit_profile'))

#         elif action == 'update_appointment':
#             appt_id = int(request.form.get('appointment_id'))
#             appointment = Appointment.query.filter_by(id=appt_id, user_id=user.id).first()

#             if appointment:
#                 appointment.fullname = request.form.get('fullname')
#                 appointment.email = request.form.get('appt_email')
#                 appointment.treatment = request.form.get('treatment')
#                 appointment.date = request.form.get('date')
#                 appointment.time = request.form.get('time')

#                 db.session.commit()
#                 flash("Appointment updated successfully!", "success")
#             else:
#                 flash("Appointment not found!", "danger")

#             return redirect(url_for('edit_profile'))

#     appointments = Appointment.query.filter_by(user_id=user.id).all()
#     return render_template('edit_profile.html', user=user, appointments=appointments)


# # ================= BLOGS PAGE =================
# @app.route('/blogs')
# def blogs():
#     images = os.listdir(app.config['UPLOAD_IMAGE_FOLDER'])
#     videos = os.listdir(app.config['UPLOAD_VIDEO_FOLDER'])
#     return render_template('blogs.html', images=images, videos=videos)


# # ================= UPLOAD MEDIA =================
# @app.route('/admin/upload', methods=['GET', 'POST'])
# @login_required
# @admin_required
# def upload_media():
#     if request.method == 'POST':
#         file = request.files.get('file')
#         file_type = request.form.get('type')

#         if not file or file.filename == '':
#             flash("No file selected", "danger")
#             return redirect(request.url)

#         filename = secure_filename(file.filename)

#         if file_type == 'image' and allowed_file(filename, ALLOWED_IMAGE):
#             file.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename))
#             flash("Image uploaded successfully!", "success")
#         elif file_type == 'video' and allowed_file(filename, ALLOWED_VIDEO):
#             file.save(os.path.join(app.config['UPLOAD_VIDEO_FOLDER'], filename))
#             flash("Video uploaded successfully!", "success")
#         else:
#             flash("Invalid file type", "danger")
#             return redirect(request.url)

#         return redirect(url_for('upload_media'))

#     images = os.listdir(app.config['UPLOAD_IMAGE_FOLDER'])
#     videos = os.listdir(app.config['UPLOAD_VIDEO_FOLDER'])
#     return render_template('upload_media.html', images=images, videos=videos)


# # ================= DELETE MEDIA =================
# @app.route('/admin/delete-media/<folder>/<filename>')
# @login_required
# @admin_required
# def delete_media(folder, filename):
#     if folder == "images":
#         path = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename)
#     elif folder == "videos":
#         path = os.path.join(app.config['UPLOAD_VIDEO_FOLDER'], filename)
#     else:
#         flash("Invalid folder", "danger")
#         return redirect(url_for('upload_media'))

#     if os.path.exists(path):
#         os.remove(path)
#         flash("Deleted successfully!", "success")
#     else:
#         flash("File not found!", "danger")

#     return redirect(url_for('upload_media'))


# # ================= REVIEWS & CONTACT =================
# @app.route('/submit-review', methods=['POST'])
# def submit_review():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     subject = request.form.get('subject')
#     message = request.form.get('message')

#     if not name or not email or not subject or not message:
#         flash("All fields are required!", "danger")
#         return redirect(request.referrer or url_for('home'))

#     review = Review(name=name, email=email, subject=subject, message=message)

#     try:
#         db.session.add(review)
#         db.session.commit()
#         flash("Message sent successfully!", "success")
#     except Exception as e:
#         db.session.rollback()
#         print("Review Error:", e)
#         flash("Something went wrong!", "danger")

#     return redirect(request.referrer or url_for('home'))


# @app.route('/admin/delete-review/<int:id>')
# @login_required
# @admin_required
# def delete_review(id):
#     review = Review.query.get_or_404(id)
#     db.session.delete(review)
#     db.session.commit()
#     flash("Review deleted successfully!", "success")
#     return redirect(url_for('admin_dashboard'))


# @app.route('/submit-contact', methods=['POST'])
# def submit_contact():
#     name = request.form.get('name')
#     email = request.form.get('email')
#     subject = request.form.get('subject')
#     message = request.form.get('message')

#     if not name or not email or not subject or not message:
#         flash("All fields are required!", "danger")
#         return redirect(url_for('contact'))

#     review = Review(name=name, email=email, subject=subject, message=message)
#     db.session.add(review)
#     db.session.commit()

#     flash("Message sent successfully!", "success")
#     return redirect(url_for('contact'))

# @app.route('/delete_treatment_log/<int:appt_id>/<int:log_index>', methods=['POST'])
# @login_required
# @admin_required
# def delete_treatment_log(appt_id, log_index):
#     appointment = Appointment.query.get_or_404(appt_id)
    
#     if appointment.notes:
#         # Saare notes ko tod kar list bana rahe hain
#         logs_array = [log.strip() for log in appointment.notes.split("|||")]
        
#         # Jo index doctor ne select kiya (jaise index 2 ya 3), use list se delete karenge
#         if 0 <= log_index < len(logs_array):
#             del logs_array[log_index]
            
#             # Agar sab delete ho gaya toh column khali, nahi toh baaki bache notes ko wapas jod do
#             if not logs_array or (len(logs_array) == 1 and logs_array[0] == "Original Client Note Placeholder"):
#                 appointment.notes = ""
#             else:
#                 appointment.notes = " ||| ".join(logs_array)
                
#             db.session.commit()
#             flash('Progress log entry deleted successfully!', 'success')
            
#     # Delete hote hi wapas dashboard usi patient ke open logs par khulega
#     return redirect(url_for('client_details', select_id=appt_id, show_logs='true'))



# from flask_mail import Mail, Message

# mail = Mail()
# mail.init_app(app)

# def send_email(to, subject, body):
#     try:
#         msg = Message(
#             subject=subject,
#             sender=app.config['MAIL_USERNAME'],
#             recipients=[to]
#         )
#         msg.body = body
#         mail.send(msg)
#         print(f"Email sent successfully to {to}")
#     except Exception as e:
#         print("MAIL ERROR:", repr(e))
#         raise



# @app.route('/forgot-password', methods=['GET', 'POST'])
# def forgot_password():
#     if request.method == 'POST':
#         email = request.form.get('email', '').strip()

#         if not email:
#             flash('Please enter your email.', 'danger')
#             return redirect(url_for('forgot_password'))

#         user = User.query.filter_by(email=email).first()

#         if not user:
#             flash('Email not found.', 'danger')
#             return redirect(url_for('forgot_password'))

#         try:
#         token = serializer.dumps(email, salt='password-reset')

#     user.reset_token = token
#     user.reset_token_used = False
#     db.session.commit()

#     base_url = os.getenv("BASE_URL", "https://yes-dental.onrender.com").rstrip("/")
#     reset_link = f"{base_url}{url_for('reset_password', token=token)}"

#     body = f"""
# Hello {user.name},

# You requested a password reset.

# Click the link below:
# {reset_link}

# This link will expire in 1 hour.

# If you did not request this, please ignore this email.

# YES Dental
# """

#     # ✅ FIXED INDENTATION (IMPORTANT)
#     threading.Thread(
#         target=send_email,
#         args=(email, "YES Dental - Password Reset", body)
#     ).start()

#     flash('Password reset link sent to your email.', 'success')
#     return redirect(url_for('login'))

# except Exception as e:
#     db.session.rollback()
#     print("FORGOT PASSWORD ERROR:", repr(e))
#     flash('Something went wrong while processing reset request.', 'danger')
#     return redirect(url_for('forgot_password'))
# # ----------------------------------------- reset password---------------------------
# # ---------------------------------- RESET PASSWORD ----------------------------------

# @app.route('/reset-password/<token>', methods=['GET', 'POST'])
# def reset_password(token):
#     try:
#         email = serializer.loads(token, salt='password-reset', max_age=3600)
#     except Exception as e:
#         print("TOKEN ERROR:", e)
#         flash('Invalid or expired reset link.', 'danger')
#         return redirect(url_for('login'))

#     user = User.query.filter_by(email=email).first()

#     if not user:
#         flash('User not found.', 'danger')
#         return redirect(url_for('login'))

#     if user.reset_token != token:
#         flash('Invalid reset link.', 'danger')
#         return redirect(url_for('login'))

#     if user.reset_token_used:
#         flash('This reset link has already been used.', 'danger')
#         return redirect(url_for('login'))

#     if request.method == 'POST':
#         password = request.form.get('password', '').strip()
#         confirm_password = request.form.get('confirm_password', '').strip()

#         if not password or not confirm_password:
#             flash('Both password fields are required.', 'danger')
#             return redirect(request.url)

#         if password != confirm_password:
#             flash('Passwords do not match.', 'danger')
#             return redirect(request.url)

#         try:
#             user.password = generate_password_hash(password)
#             user.reset_token_used = True
#             user.reset_token = None
#             db.session.commit()

#             flash('Password updated successfully. Please login.', 'success')
#             return redirect(url_for('login'))

#         except Exception as e:
#             db.session.rollback()
#             print("RESET PASSWORD ERROR:", e)
#             flash('Failed to reset password.', 'danger')
#             return redirect(request.url)

#     return render_template('reset_password.html')

# if __name__ == '__main__':
#     app.run(debug=True)
import os
import sys
import threading  # Required for threading in forgot_password
from datetime import datetime
from functools import wraps

from dotenv import load_dotenv
from flask import Flask, flash, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_mail import Mail, Message
from flask_sqlalchemy import SQLAlchemy
from itsdangerous import URLSafeTimedSerializer
from sqlalchemy import create_engine
from werkzeug.security import check_password_hash, generate_password_hash
from werkzeug.utils import secure_filename

# Import models
from models import Appointment, Review, User, db

load_dotenv()

# =====================================================================
# 1. APP CONFIGURATION & INITIALIZATION
# =====================================================================

app = Flask(__name__)

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'my-dev-secret-key')

# Mail Setup
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER', 'smtp.gmail.com')
app.config['MAIL_PORT'] = int(os.getenv('MAIL_PORT', 587))
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
mail = Mail()
mail.init_app(app)

# Database Setup
MYSQL_USER = os.getenv("MYSQL_USER")
MYSQL_PASSWORD = os.getenv("MYSQL_PASSWORD")
MYSQL_HOST = os.getenv("MYSQL_HOST")
MYSQL_PORT = os.getenv("MYSQL_PORT", "3307")
MYSQL_DB = os.getenv("MYSQL_DB")
app.config['SQLALCHEMY_DATABASE_URI'] = (
    f"mysql+mysqlconnector://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DB}"
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

engine = create_engine(
    app.config['SQLALCHEMY_DATABASE_URI'],
    pool_pre_ping=True,
    pool_recycle=280,
    pool_size=5,
    max_overflow=10
)

# Folders Configuration
UPLOAD_IMAGE_FOLDER = 'static/images'
UPLOAD_VIDEO_FOLDER = 'static/videos'
app.config['UPLOAD_IMAGE_FOLDER'] = UPLOAD_IMAGE_FOLDER
app.config['UPLOAD_VIDEO_FOLDER'] = UPLOAD_VIDEO_FOLDER

ALLOWED_IMAGE = {'png', 'jpg', 'jpeg'}
ALLOWED_VIDEO = {'mp4', 'mov', 'avi'}

# Login Manager Setup
login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.login_message = "Please log in to access this page."


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# DB Initialization Execution
try:
    print("Connecting to MySQL...")
    db.init_app(app)
    with app.app_context():
        db.create_all()
    print("Database connected successfully!")
except Exception as e:
    print("CRITICAL ERROR: Database connection failed")
    print(e)


# =====================================================================
# 2. HELPER FUNCTIONS & DECORATORS
# =====================================================================

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated or not getattr(current_user, "is_admin", False):
            flash("Admin access required", "danger")
            return redirect(url_for("home"))
        return f(*args, **kwargs)
    return wrapper


def allowed_file(filename, allowed_set):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_set


def send_email(app_instance, to, subject, body):
    """
    Sends email within the explicit application context required 
    by background threads running Flask-Mail.
    """
    try:
        with app_instance.app_context():
            msg = Message(
                subject=subject,
                sender=app_instance.config['MAIL_USERNAME'],
                recipients=[to]
            )
            msg.body = body
            mail.send(msg)
            print(f"Email sent successfully to {to}")
    except Exception as e:
        print("MAIL ERROR:", repr(e))
        raise


# =====================================================================
# 3. PUBLIC CORE ROUTES
# =====================================================================

@app.route('/')
def home():
    return render_template('pages.html')


@app.route('/services')
def services():
    return render_template('services.html')


@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/team')
def team():
    return render_template('team.html')


@app.route('/contact', methods=['GET'])
def contact():
    return render_template('contact.html')


@app.route('/blogs')
def blogs():
    images = os.listdir(app.config['UPLOAD_IMAGE_FOLDER'])
    videos = os.listdir(app.config['UPLOAD_VIDEO_FOLDER'])
    return render_template('blogs.html', images=images, videos=videos)


# =====================================================================
# 4. AUTHENTICATION / PASSWORD RESET ROUTES
# =====================================================================

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        name = request.form.get('name')
        password = request.form.get('password')

        if User.query.filter_by(email=email).first():
            flash("Email already exists", "danger")
            return redirect(url_for('register'))

        user = User(
            email=email,
            name=name,
            password=generate_password_hash(password)
        )

        db.session.add(user)
        db.session.commit()

        flash("Registered successfully. Please login.", "success")
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))

    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        remember = bool(request.form.get('remember'))

        user = User.query.filter_by(email=email).first()

        if not user or not check_password_hash(user.password, password):
            flash("Invalid credentials", "danger")
            return redirect(url_for('login'))

        login_user(user, remember=remember)
        return redirect(url_for('dashboard'))

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", "info")
    return redirect(url_for('home'))


@app.route('/forgot-password', methods=['GET', 'POST'])
def forgot_password():
    if request.method == 'POST':
        email = request.form.get('email', '').strip()

        if not email:
            flash('Please enter your email.', 'danger')
            return redirect(url_for('forgot_password'))

        user = User.query.filter_by(email=email).first()

        if not user:
            flash('Email not found.', 'danger')
            return redirect(url_for('forgot_password'))

        try:
            token = serializer.dumps(email, salt='password-reset')
            user.reset_token = token
            user.reset_token_used = False
            db.session.commit()

            base_url = os.getenv("BASE_URL", "https://yes-dental.onrender.com").rstrip("/")
            reset_link = f"{base_url}{url_for('reset_password', token=token)}"

            body = f"""
Hello {user.name},

You requested a password reset.

Click the link below:
{reset_link}

This link will expire in 1 hour.

If you did not request this, please ignore this email.

YES Dental
"""

            # Explicitly passing the 'app' instance so the background thread maintains context
            threading.Thread(
                target=send_email,
                args=(app, email, "YES Dental - Password Reset", body)
            ).start()

            flash('Password reset link sent to your email.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            print("FORGOT PASSWORD ERROR:", repr(e))
            flash('Something went wrong while processing reset request.', 'danger')
            return redirect(url_for('forgot_password'))
            
    return render_template('forgot_password.html')


@app.route('/reset-password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        email = serializer.loads(token, salt='password-reset', max_age=3600)
    except Exception as e:
        print("TOKEN ERROR:", e)
        flash('Invalid or expired reset link.', 'danger')
        return redirect(url_for('login'))

    user = User.query.filter_by(email=email).first()

    if not user:
        flash('User not found.', 'danger')
        return redirect(url_for('login'))

    if user.reset_token != token:
        flash('Invalid reset link.', 'danger')
        return redirect(url_for('login'))

    if user.reset_token_used:
        flash('This reset link has already been used.', 'danger')
        return redirect(url_for('login'))

    if request.method == 'POST':
        password = request.form.get('password', '').strip()
        confirm_password = request.form.get('confirm_password', '').strip()

        if not password or not confirm_password:
            flash('Both password fields are required.', 'danger')
            return redirect(request.url)

        if password != confirm_password:
            flash('Passwords do not match.', 'danger')
            return redirect(request.url)

        try:
            user.password = generate_password_hash(password)
            user.reset_token_used = True
            user.reset_token = None
            db.session.commit()

            flash('Password updated successfully. Please login.', 'success')
            return redirect(url_for('login'))

        except Exception as e:
            db.session.rollback()
            print("RESET PASSWORD ERROR:", e)
            flash('Failed to reset password.', 'danger')
            return redirect(request.url)

    return render_template('reset_password.html')


# =====================================================================
# 5. USER CLIENT DASHBOARD & PROFILE MANAGEMENT
# =====================================================================

@app.route('/dashboard')
@login_required
def dashboard():
    if getattr(current_user, "is_admin", False):
        return redirect(url_for("admin_dashboard"))

    appointments = Appointment.query.filter_by(
        user_id=current_user.id,
        is_deleted=False
    ).order_by(Appointment.id.desc()).all()
    return render_template('dashboard.html', name=current_user.name, appointments=appointments)


@app.route('/my-profile', methods=['GET', 'POST'])
@login_required
def my_profile():
    user = current_user

    if request.method == 'POST':
        new_name = request.form.get('name')
        new_email = request.form.get('email')

        existing_user = User.query.filter_by(email=new_email).first()
        if existing_user and existing_user.id != user.id:
            flash("Email already exists!", "danger")
            return redirect(url_for('my_profile'))

        user.name = new_name
        user.email = new_email
        db.session.commit()

        flash("Profile updated successfully!", "success")
        return redirect(url_for('my_profile'))

    appointments = Appointment.query.filter_by(user_id=user.id).all()
    total = len(appointments)
    pending = len([a for a in appointments if a.status == 'pending'])
    confirmed = len([a for a in appointments if a.status == 'confirmed'])
    recent_appointments = appointments[-3:][::-1]

    return render_template(
        'my_profile.html',
        total=total,
        pending=pending,
        confirmed=confirmed,
        recent_appointments=recent_appointments,
        user=user
    )


@app.route('/profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    user = current_user

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'update_user':
            new_name = request.form.get('name')
            new_email = request.form.get('email')

            existing = User.query.filter_by(email=new_email).first()
            if existing and existing.id != user.id:
                flash("Email already exists!", "danger")
                return redirect(url_for('edit_profile'))

            user.name = new_name
            user.email = new_email
            db.session.commit()
            flash("Profile updated successfully!", "success")
            return redirect(url_for('edit_profile'))

        elif action == 'update_appointment':
            appt_id = int(request.form.get('appointment_id'))
            appointment = Appointment.query.filter_by(id=appt_id, user_id=user.id).first()

            if appointment:
                appointment.fullname = request.form.get('fullname')
                appointment.email = request.form.get('appt_email')
                appointment.treatment = request.form.get('treatment')
                appointment.date = request.form.get('date')
                appointment.time = request.form.get('time')

                db.session.commit()
                flash("Appointment updated successfully!", "success")
            else:
                flash("Appointment not found!", "danger")

            return redirect(url_for('edit_profile'))

    appointments = Appointment.query.filter_by(user_id=user.id).all()
    return render_template('edit_profile.html', user=user, appointments=appointments)


@app.route('/treatment-history')
@login_required
def treatment_history():
    appointments = Appointment.query.filter_by(user_id=current_user.id).all()
    return render_template('treatment_history.html', appointments=appointments, name=current_user.name)


# =====================================================================
# 6. BOOKING SUBMISSIONS (PUBLIC/CLIENT)
# =====================================================================

@app.route('/booking')
def booking_page():
    return render_template('booking.html')


@app.route('/submit-booking', methods=['POST'])
def submit_booking():
    try:
        appointment = Appointment(
            user_id=current_user.id if current_user.is_authenticated else None,
            fullname=request.form.get('fullname'),
            phone=request.form.get('phone'),
            email=request.form.get('email'),
            address=request.form.get('address'),
            date=request.form.get('date'),
            time=request.form.get('time'),
            treatment=request.form.get('treatment'),
            service_type=(request.form.get("service_type") or "").strip(),
            specialist=(request.form.get("specialist") or "").strip(),
            notes=request.form.get('notes'),
            status='pending'
        )

        db.session.add(appointment)
        db.session.commit()

        flash("Appointment booked successfully!", "success")
        return redirect(url_for('booking_page'))

    except Exception as e:
        db.session.rollback()
        print("Booking Error:", e)
        flash("Booking failed. Try again.", "danger")
        return redirect(url_for('booking_page'))


# =====================================================================
# 7. ADMIN CORE DASHBOARD & CONTROL SYSTEM
# =====================================================================

@app.route('/admin/dashboard')
@login_required
@admin_required
def admin_dashboard():
    appointments = Appointment.query.filter_by(
        is_deleted=False
    ).order_by(Appointment.id.desc()).all()

    reviews = Review.query.order_by(Review.id.desc()).all()

    return render_template(
        'admin_dashboard.html',
        appointments=appointments,
        reviews=reviews
    )


@app.route('/admin/client-details')
@login_required
@admin_required
def client_details():
    appointments = Appointment.query.filter_by(
        is_deleted=False
    ).order_by(Appointment.id.desc()).all()
    
    target_id = request.args.get('select_id', type=int)
    show_logs = request.args.get('show_logs', 'false')
    
    return render_template(
        'client_details.html', 
        appointments=appointments, 
        target_id=target_id,
        show_logs=show_logs
    )


@app.route('/admin/appointment/<int:appt_id>/update', methods=['POST'])
@login_required
@admin_required
def update_appointment(appt_id):
    appointment = Appointment.query.get_or_404(appt_id)
    
    new_note = request.form.get('notes', '').strip()
    status = request.form.get('status')
    
    if status:
        appointment.status = status.strip()
        
    if new_note:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        formatted_new_note = f"[{current_time}] {new_note}"
        
        existing_notes = appointment.notes if appointment.notes else ""
        
        for s in ["Pending", "Confirmed", "Rejected", "Completed"]:
            if existing_notes.endswith(s) and not existing_notes.endswith(f"||| {s}"):
                existing_notes = existing_notes[:-len(s)].strip()
        
        if existing_notes:
            appointment.notes = f"{existing_notes} ||| {formatted_new_note}"
        else:
            appointment.notes = formatted_new_note
            
    db.session.commit()
    flash('Patient profile updated successfully!', 'success')
    
    return redirect(url_for('admin_dashboard', select_id=appt_id))


@app.route('/admin/settings', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_settings():
    admin = current_user

    if request.method == 'POST':
        action = request.form.get('action')

        if action == 'change_email':
            new_email = request.form.get('email')
            existing_user = User.query.filter_by(email=new_email).first()

            if existing_user and existing_user.id != admin.id:
                flash('Email already exists!', 'danger')
            else:
                admin.email = new_email
                db.session.commit()
                flash('Email updated successfully!', 'success')

        elif action == 'change_password':
            current_password = request.form.get('current_password', '').strip()
            new_password = request.form.get('new_password', '').strip()
            confirm_password = request.form.get('confirm_password', '').strip()

            if not current_password or not new_password or not confirm_password:
                flash('All fields are required!', 'danger')
            elif not check_password_hash(admin.password, current_password):
                flash('Current password is incorrect!', 'danger')
            elif new_password != confirm_password:
                flash('Passwords do not match!', 'danger')
            else:
                admin.password = generate_password_hash(new_password)
                db.session.commit()
                flash('Password updated successfully!', 'success')

    return render_template('admin_settings.html', admin=admin)


# =====================================================================
# 8. CLINICAL TREATMENT LOG EXTENSIONS (ADMIN)
# =====================================================================

@app.route('/add_treatment_log/<int:appt_id>', methods=['POST'])
@login_required
@admin_required
def add_treatment_log(appt_id):
    appointment = Appointment.query.get_or_404(appt_id)
    new_note = request.form.get('doctor_note', '').strip()
    
    if not new_note:
        flash("Clinical progress note cannot be empty!", "danger")
        return redirect(url_for('client_details', select_id=appt_id))
        
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_new_note = f"[{current_time}] {new_note}"
    
    existing_notes = appointment.notes if appointment.notes else ""
    
    for s in ["Pending", "Confirmed", "Rejected", "Completed"]:
        if existing_notes.endswith(s) and not existing_notes.endswith(f"||| {s}"):
            existing_notes = existing_notes[:-len(s)].strip()
            
    if existing_notes:
        appointment.notes = f"{existing_notes} ||| {formatted_new_note}"
    else:
        appointment.notes = f"Original Client Note Placeholder ||| {formatted_new_note}"
        
    try:
        db.session.commit()
        flash('Progress note committed and clinical dashboard synced successfully!', 'success')
    except Exception as e:
        db.session.rollback()
        print("Treatment log error details:", e)
        flash('Failed to save progress log context structural update.', 'danger')
    
    return redirect(url_for('client_details', select_id=appt_id, show_logs='true'))


@app.route('/delete_treatment_log/<int:appt_id>/<int:log_index>', methods=['POST'])
@login_required
@admin_required
def delete_treatment_log(appt_id, log_index):
    appointment = Appointment.query.get_or_404(appt_id)
    
    if appointment.notes:
        logs_array = [log.strip() for log in appointment.notes.split("|||")]
        
        if 0 <= log_index < len(logs_array):
            del logs_array[log_index]
            
            if not logs_array or (len(logs_array) == 1 and logs_array[0] == "Original Client Note Placeholder"):
                appointment.notes = ""
            else:
                appointment.notes = " ||| ".join(logs_array)
                
            db.session.commit()
            flash('Progress log entry deleted successfully!', 'success')
            
    return redirect(url_for('client_details', select_id=appt_id, show_logs='true'))


# =====================================================================
# 9. APPOINTMENT MANAGEMENT SYSTEM (SOFT/HARD DELETE/RESTORE)
# =====================================================================

@app.route('/admin/delete_appointment/<int:id>')
@login_required
@admin_required
def delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    appointment.is_deleted = True
    db.session.commit()
    
    flash("Appointment moved to trash (soft deleted).", "warning")
    return redirect(url_for("admin_dashboard"))


@app.route('/admin/permanently_delete/<int:id>')
@login_required
@admin_required
def permanently_delete_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    
    if not appointment.is_deleted:
        flash("Cannot permanently delete an active appointment. Please delete it first.", "danger")
        return redirect(url_for("admin_dashboard"))

    db.session.delete(appointment)
    db.session.commit()
    
    flash("Appointment permanently deleted.", "danger")
    return redirect(url_for("admin_dashboard"))


@app.route('/admin/restore_appointment/<int:id>')
@login_required
@admin_required
def restore_appointment(id):
    appointment = Appointment.query.get_or_404(id)
    
    if not appointment.is_deleted:
        flash("This appointment is not in trash.", "warning")
        return redirect(url_for("admin_dashboard"))

    appointment.is_deleted = False
    db.session.commit()
    
    flash("Appointment restored successfully.", "success")
    return redirect(url_for("admin_dashboard"))


@app.route('/admin/trash')
@login_required
@admin_required
def admin_trash():
    appointments = Appointment.query.filter_by(is_deleted=True).order_by(Appointment.id.desc()).all()
    return render_template('admin_trash.html', appointments=appointments)


# =====================================================================
# 10. MEDIA UPLOAD & CONTROL (ADMIN)
# =====================================================================

@app.route('/admin/upload', methods=['GET', 'POST'])
@login_required
@admin_required
def upload_media():
    if request.method == 'POST':
        file = request.files.get('file')
        file_type = request.form.get('type')

        if not file or file.filename == '':
            flash("No file selected", "danger")
            return redirect(request.url)

        filename = secure_filename(file.filename)

        if file_type == 'image' and allowed_file(filename, ALLOWED_IMAGE):
            file.save(os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename))
            flash("Image uploaded successfully!", "success")
        elif file_type == 'video' and allowed_file(filename, ALLOWED_VIDEO):
            file.save(os.path.join(app.config['UPLOAD_VIDEO_FOLDER'], filename))
            flash("Video uploaded successfully!", "success")
        else:
            flash("Invalid file type", "danger")
            return redirect(request.url)

        return redirect(url_for('upload_media'))

    images = os.listdir(app.config['UPLOAD_IMAGE_FOLDER'])
    videos = os.listdir(app.config['UPLOAD_VIDEO_FOLDER'])
    return render_template('upload_media.html', images=images, videos=videos)


@app.route('/admin/delete-media/<folder>/<filename>')
@login_required
@admin_required
def delete_media(folder, filename):
    if folder == "images":
        path = os.path.join(app.config['UPLOAD_IMAGE_FOLDER'], filename)
    elif folder == "videos":
        path = os.path.join(app.config['UPLOAD_VIDEO_FOLDER'], filename)
    else:
        flash("Invalid folder", "danger")
        return redirect(url_for('upload_media'))

    if os.path.exists(path):
        os.remove(path)
        flash("Deleted successfully!", "success")
    else:
        flash("File not found!", "danger")

    return redirect(url_for('upload_media'))


# =====================================================================
# 11. REVIEWS & FEEDBACK MANAGEMENT
# =====================================================================

@app.route('/submit-review', methods=['POST'])
def submit_review():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not name or not email or not subject or not message:
        flash("All fields are required!", "danger")
        return redirect(request.referrer or url_for('home'))

    review = Review(name=name, email=email, subject=subject, message=message)

    try:
        db.session.add(review)
        db.session.commit()
        flash("Message sent successfully!", "success")
    except Exception as e:
        db.session.rollback()
        print("Review Error:", e)
        flash("Something went wrong!", "danger")

    return redirect(request.referrer or url_for('home'))


@app.route('/submit-contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    subject = request.form.get('subject')
    message = request.form.get('message')

    if not name or not email or not subject or not message:
        flash("All fields are required!", "danger")
        return redirect(url_for('contact'))

    review = Review(name=name, email=email, subject=subject, message=message)
    db.session.add(review)
    db.session.commit()

    flash("Message sent successfully!", "success")
    return redirect(url_for('contact'))


@app.route('/admin/reviews')
@login_required
@admin_required
def admin_Reviews():
    reviews = Review.query.order_by(Review.id.desc()).all()
    return render_template('admin_Reviews.html', reviews=reviews)


@app.route('/admin/delete-review/<int:id>')
@login_required
@admin_required
def delete_review(id):
    review = Review.query.get_or_404(id)
    db.session.delete(review)
    db.session.commit()
    flash("Review deleted successfully!", "success")
    return redirect(url_for('admin_dashboard'))


# =====================================================================
# 12. RUN APPLICATION
# =====================================================================

if __name__ == '__main__':
    app.run(debug=True)