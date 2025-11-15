from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'supersecretkey'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

# ------------------------------
# LOGIN MANAGER SETUP
# ------------------------------
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# ------------------------------
# DATABASE MODELS
# ------------------------------
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# ------------------------------
# ROUTES
# ------------------------------

@app.route('/')
def index():
    return render_template('index.html')

# ---------- REGISTER ----------
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        hashed_pw = generate_password_hash(password, method='pbkdf2:sha256')

        existing_user = User.query.filter((User.username == username) | (User.email == email)).first()
        if existing_user:
            flash('Username or email already exists!', 'error')
            return redirect(url_for('register'))

        new_user = User(username=username, email=email, password=hashed_pw)
        db.session.add(new_user)
        db.session.commit()
        flash('Account created! You can now log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

# ---------- LOGIN ----------
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()

        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Logged in successfully!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password!', 'error')
            return redirect(url_for('login'))
    return render_template('login.html')

# ---------- DASHBOARD ----------
@app.route('/dashboard')
@login_required
def dashboard():
    users = User.query.all()
    return render_template('users.html', user=current_user, users=users)

# ---------- LOGOUT ----------
@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

# ======== FORGOT PASSWORD =========
@app.route('/forgot_password', methods=['GET', 'POST'])
def forgot_password():
    from werkzeug.security import generate_password_hash

    message = None
    category = None

    if request.method == 'POST':
        email = request.form['email']
        new_password = request.form['new_password']
        user = User.query.filter_by(email=email.lower().strip()).first()

        if user:
            user.password = generate_password_hash(new_password, method='pbkdf2:sha256')
            db.session.commit()
            message = '✅ Password has been reset successfully! You can now log in.'
            category = 'success'
        else:
            message = '❌ Email not found. Please check and try again.'
            category = 'danger'

    if message:
        flash(message, category)
        # Auto redirect after successful reset
        if category == 'success':
            return redirect(url_for('login'))

    return render_template('forgot_password.html')

# ---------- API (OPTIONAL) ----------
@app.route('/api/users', methods=['GET'])
def api_get_users():
    all_users = User.query.all()
    return jsonify([{'id': u.id, 'username': u.username, 'email': u.email} for u in all_users])

    # ===================== USERS PAGE =====================
@app.route('/users')
@login_required
def users():
    users = User.query.all()
    return render_template('users.html', users=users)

# ------------------------------
# RUN
# ------------------------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
