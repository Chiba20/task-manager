from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask ( __name__ )
# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app . config [ 'SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Initialize database
db = SQLAlchemy ( app )

from datetime import datetime
class Task(db.Model):
     # Table name
     __tablename__ = 'tasks'
     # Columns
     id = db.Column(db.Integer, primary_key=True)
     title = db.Column(db.String(100), nullable=False)
     description = db.Column(db.Text)
     completed = db.Column(db.Boolean, default=False)
     created_at = db.Column(db.DateTime, default=datetime.utcnow)
     def to_dict(self):
         return {
         'id': self.id,
         'title': self.title,
         'description': self.description,
         'completed': self.completed,
         'created_at': self.created_at.isoformat()
     }

# Add before routes
with app.app_context():
    db.create_all()
    print("Database tables created!")

@app.route('/api/tasks', methods=['POST'])
def create_task():
     data = request.get_json()
     # Validation
     if not data or 'title' not in data:
        return jsonify({'error': 'Title is required'}), 400
     # Create new task object
     new_task = Task(
        title=data['title'],
        description=data.get('description', '')
     )
     # Add to database
     db.session.add(new_task)
     db.session.commit()
     return jsonify(new_task.to_dict()), 201


@app.route('/api/tasks', methods=['GET'])
def get_tasks():
     tasks = Task.query.all()
     return jsonify({
     'tasks': [task.to_dict() for task in tasks],
     'count': len(tasks)
     }), 200


@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
     task = Task.query.get_or_404(task_id)
     return jsonify(task.to_dict()), 200


if __name__ == '__main__':
    # server will run on port 5000
    app.run(host='0.0.0.0', port=5050, debug=True)
