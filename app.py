from flask import Flask, jsonify, request

app = Flask(__name__)

@app.route('/')
def home():
    return jsonify ({
    'message': 'Welcome to Task Manager API',
    'status': 'running'
    })

@app.route('/hello')
def hello():
    return jsonify ({
    'message': 'Hello, World!'})

@app.route('/api/status')
def status():
    return jsonify ({
    'database': 'connected',
    'server': 'running',
    'uptime': '24 hours'
    })

@app.route('/api/greet')
def greet():
    name = request.args.get('name','Guest')

    return jsonify ({
    'message': f'Hello, {name}!',
    'greeting': 'Welcome to Task Manager'
    })

@app.route('/api/add')
def add():
    # Get 'a' and 'b' from query parameters
    a = request.args.get('a', 1)
    b = request.args.get('b', 1)

    # Convert them to integers
    a = int(a)
    b = int(b)

    # Add them together
    c = a + b

    # Return the result as JSON
    return jsonify({
        'result': c,
        'operation': 'addition'
    })


@app.route('/api/tasks', methods=['POST'])
def create_task():
 # Get JSON data from request body
    data = request.get_json()
 # Access the data
    title = data.get('title')
    description = data.get('description')
 # Process and return response
    return jsonify({ 'message': 'Task created successfully','task': {
      'title': title,
      'description': description
 }
 }), 201 # 201 = Created


tasks = [] # Global list to store tasks
task_id_counter = 1 # To generate unique IDs
@app.route('/api/task', methods=['POST'])
def creates_task():
    global task_id_counter
    data = request.get_json()

    new_task = {
    'id': task_id_counter,
    'title': data.get('title'),
    'description': data.get('description'),
    'completed': False
    }
    tasks.append(new_task)
    task_id_counter += 1
    return jsonify(new_task), 201


@app . route ('/api/task', methods =['GET'])
def get_tasks () :
 return jsonify ({
  'tasks': tasks ,
  'count': len ( tasks )
}) , 200

# Get task by ID
@app.route('/api/tasks/<int:task_id>', methods=['GET'])
def get_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404
    return jsonify(task), 200


# Update a task
@app.route('/api/tasks/<int:task_id>', methods=['PUT'])
def update_task(task_id):
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    data = request.get_json()
    task['title'] = data.get('title', task['title'])
    task['description'] = data.get('description', task['description'])
    task['completed'] = data.get('completed', task['completed'])

    return jsonify({
        'message': 'Task updated successfully',
        'task': task
    }), 200


# Delete a task
@app.route('/api/tasks/<int:task_id>', methods=['DELETE'])
def delete_task(task_id):
    global tasks
    task = next((t for t in tasks if t['id'] == task_id), None)
    if task is None:
        return jsonify({'error': 'Task not found'}), 404

    tasks = [t for t in tasks if t['id'] != task_id]
    return jsonify({'message': f'Task {task_id} deleted successfully'}), 200


if __name__ == '__main__':
    app.run(debug=True, port=5000)
