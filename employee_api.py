from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app = Flask(__name__, template_folder='templates')
# Database config
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Database Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(200), nullable=False)
    date_added = db.Column(db.DateTime, default=datetime.utcnow)

# Home route
from flask import Flask, jsonify, request, render_template
# (Make sure render_template is imported at the top!)
# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Users page
@app.route('/users')
@app.route('/users')
def show_users_page():
    return render_template('users.html')
# Get all users
@app.route('/api/users', methods=['GET'])
def get_users():
    users = User.query.all()
    user_list = []
    for user in users:
        user_list.append({
            "id": user.id,
            "name": user.name,
            "email": user.email,
            "date_added": user.date_added.strftime("%Y-%m-%d %H:%M:%S")
        })
    return jsonify(user_list)

# Add new user
@app.route('/api/users', methods=['POST'])
def add_user():
    data = request.get_json()
    new_user = User(name=data['name'], email=data['email'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User added successfully!"}), 201

# Delete a user
@app.route('/api/users/<int:id>', methods=['DELETE'])
def api_delete_user(id):
    user = User.query.get_or_404(id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({"message": f"User {id} deleted successfully!"})
# Update a user
# Update a user
@app.route('/api/users/<int:id>', methods=['PUT'])
def api_update_user(id):
    user = User.query.get_or_404(id)
    data = request.get_json()

    user.name = data.get('name', user.name)
    user.email = data.get('email', user.email)
    db.session.commit()

    return jsonify({"message": f"User {id} updated successfully!"})
if __name__ == "__main__":
    app.run(debug=True)
@app.route('/users')
def users_page():
    return render_template('users.html')

@app.route('/edit.html')
def edit_page():
    return render_template('edit.html')
