# app_with_mysql_db.py
from flask import Flask, request, jsonify, abort
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from datetime import datetime
import os

app = Flask(__name__)

# Use the exact URI you were given
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:passw0rd@localhost:3308/app_db?charset=utf8mb4'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# -----------------------
# Part 1: Models
# -----------------------
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)

    # relationship to tasks
    tasks = db.relationship('Task', backref='user', cascade='all, delete-orphan', lazy=True)

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'created_at': self.created_at.isoformat()
        }

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow, nullable=False)
    # Part 3: link to user
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'created_at': self.created_at.isoformat(),
            'user_id': self.user_id
        }

# Create tables if not exist
with app.app_context():
    db.create_all()

# -----------------------
# Part 2: User CRUD Endpoints
# -----------------------

# POST /api/users - create user
@app.route('/api/users', methods=['POST'])
def create_user():
    data = request.get_json() or {}
    username = data.get('username', '').strip()
    email = data.get('email', '').strip()

    if not username or not email:
        return jsonify({'error': 'username and email are required'}), 400

    # Check uniqueness
    if User.query.filter((User.username == username) | (User.email == email)).first():
        return jsonify({'error': 'username or email already exists'}), 409

    user = User(username=username, email=email)
    db.session.add(user)
    db.session.commit()
    return jsonify(user.to_dict()), 201

# GET /api/users - list all users
@app.route('/api/users', methods=['GET'])
def list_users():
    users = User.query.order_by(User.id).all()
    return jsonify([u.to_dict() for u in users]), 200

# GET /api/users/<id> - get single user
@app.route('/api/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.get_or_404(user_id)
    return jsonify(user.to_dict()), 200

# PUT /api/users/<id> - update user
@app.route('/api/users/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get_or_404(user_id)
    data = request.get_json() or {}

    username = data.get('username')
    email = data.get('email')

    if username:
        username = username.strip()
        if username == '':
            return jsonify({'error': 'username cannot be empty'}), 400
        # uniqueness check
        other = User.query.filter(User.username == username, User.id != user_id).first()
        if other:
            return jsonify({'error': 'username already used'}), 409
        user.username = username

    if email:
        email = email.strip()
        if email == '':
            return jsonify({'error': 'email cannot be empty'}), 400
        other = User.query.filter(User.email == email, User.id != user_id).first()
        if other:
            return jsonify({'error': 'email already used'}), 409
        user.email = email

    db.session.commit()
    return jsonify(user.to_dict()), 200

# DELETE /api/users/<id> - delete user (also deletes tasks via cascade)
@app.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get_or_404(user_id)
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': f'User {user_id} deleted'}), 200

# -----------------------
# Part 3: Tasks + Link to Users
# -----------------------

# POST /api/tasks - create task (accept user_id)
@app.route('/api/tasks', methods=['POST'])
def create_task():
    data = request.get_json() or {}
    title = (data.get('title') or '').strip()
    description = data.get('description')
    user_id = data.get('user_id')  # optional but accepted

    if not title:
        return jsonify({'error': 'title is required'}), 400

    # If user_id provided, validate it exists
    if user_id is not None:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': f'user_id {user_id} does not exist'}), 400

    task = Task(title=title, description=description, user_id=user_id)
    db.session.add(task)
    db.session.commit()
    return jsonify(task.to_dict()), 201

# GET /api/tasks - list all tasks
@app.route('/api/tasks', methods=['GET'])
def list_tasks():
    tasks = Task.query.order_by(Task.id).all()
    return jsonify([t.to_dict() for t in tasks]), 200

# GET /api/tasks/<id> - get single task
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = Task.query.get_or_404(task_id)
    return jsonify(task.to_dict()), 200

# PUT /api/tasks/<id> - update task (you can change user_id here too)
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = Task.query.get_or_404(task_id)
    data = request.get_json() or {}
    title = data.get('title')
    description = data.get('description')
    user_id = data.get('user_id')

    if title is not None:
        t = title.strip()
        if t == '':
            return jsonify({'error': 'title cannot be empty'}), 400
        task.title = t

    if description is not None:
        task.description = description

    if user_id is not None:
        user = User.query.get(user_id)
        if not user:
            return jsonify({'error': f'user_id {user_id} does not exist'}), 400
        task.user_id = user_id

    db.session.commit()
    return jsonify(task.to_dict()), 200

# DELETE /api/tasks/<id>
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': f'Task {task_id} deleted'}), 200

# GET /api/users/<id>/tasks - all tasks for a user
@app.route('/api/users/<int:user_id>/tasks', methods=['GET'])
def tasks_for_user(user_id):
    user = User.query.get_or_404(user_id)
    tasks = Task.query.filter_by(user_id=user_id).order_by(Task.id).all()
    return jsonify([t.to_dict() for t in tasks]), 200

# health check
@app.route('/health', methods=['GET'])
def health():
    # quick db query to ensure connection
    try:
        # one lightweight query
        count = db.session.query(func.count(User.id)).scalar()
        return jsonify({'status': 'ok', 'user_count': count}), 200
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

if __name__ == '__main__':
    # Run on port 5050 (change if needed)
    app.run(host='0.0.0.0', port=5050, debug=True)
