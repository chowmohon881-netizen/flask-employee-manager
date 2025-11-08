from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

# Database setup
import os

# Build a full path for the database that works locally & on Render
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "users.db")
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{db_path}"

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
print("✅ Database path:", db_path)

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    name = request.form['name'].strip()
    email = request.form['email'].strip()

    # Validation checks
    if not name or not email:
        return "⚠️ Error: Name and Email cannot be empty."

    existing_user = User.query.filter_by(email=email).first()
    if existing_user:
        return "⚠️ Error: This email already exists. Try another."

    # If all good, save to database
    user = User(name=name, email=email)
    db.session.add(user)
    db.session.commit()
    return redirect(url_for('show_users'))


@app.route('/users')
def show_users():
    users = User.query.order_by(User.date_added.desc()).all()
    return render_template('users.html', users=users)

@app.route('/delete_user/<int:id>')
def delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return redirect(url_for('show_users'))

# Edit user route (show the edit form)
@app.route('/edit_user/<int:id>')
def edit_user(id):
    user = User.query.get_or_404(id)
    return render_template('edit.html', user=user)

# Update user route (handle form submission)
@app.route('/update_user/<int:id>', methods=['POST'])
# Update user route (handle form submission)
@app.route('/update_user/<int:id>', methods=['POST'])
def update_user(id):
    user = User.query.get_or_404(id)
    name = request.form['name'].strip()
    email = request.form['email'].strip()

    # Validation
    if not name or not email:
        return "⚠️ Error: Name and Email cannot be empty."

    # Check if the new email belongs to another employee
    existing_user = User.query.filter_by(email=email).first()
    if existing_user and existing_user.id != user.id:
        return "⚠️ Error: This email is already used by another employee."

    # Update and save changes
    user.name = name
    user.email = email
    db.session.commit()

    return redirect(url_for('show_users'))



if __name__ == '__main__':
    app.run(debug=True)
