from flask import Flask, jsonify, request
from datetime import datetime

app = Flask(__name__)

# In-memory data storage
tasks = []
categories = []
task_id_counter = 1


# Part 1: Add Categories to Tasks


@app.route('/api/categories', methods=['POST'])
def add_category():
    data = request.get_json()
    category_name = data.get('name')
    if category_name not in categories:
        categories.append(category_name)
    return jsonify({'categories': categories})

@app.route('/api/categories', methods=['GET'])
def get_categories():
    return jsonify({'categories': categories})

@app.route('/api/tasks', methods=['POST'])
def add_task():
    global task_id_counter
    data = request.get_json()
    task = {
        'id': task_id_counter,
        'title': data.get('title'),
        'completed': False,
        'category': data.get('category'),
        'due_date': data.get('due_date'),
        'priority': data.get('priority', 'medium')
    }
    tasks.append(task)
    task_id_counter += 1
    return jsonify(task)

@app.route('/api/tasks', methods=['GET'])
def get_tasks():
    category = request.args.get('category')
    if category:
        filtered_tasks = [t for t in tasks if t['category'] == category]
        return jsonify({'tasks': filtered_tasks})
    return jsonify({'tasks': tasks})


# Part 2: Add Due Dates

@app.route('/api/tasks/overdue', methods=['GET'])
def get_overdue_tasks():
    now = datetime.now()
    overdue = []
    for task in tasks:
        if task['due_date']:
            due = datetime.strptime(task['due_date'], '%Y-%m-%d')
            if due < now and not task['completed']:
                overdue.append(task)
    return jsonify({'overdue_tasks': overdue})


# Part 3: Statistics Endpoint

@app.route('/api/tasks/stats', methods=['GET'])
def task_stats():
    total = len(tasks)
    completed = len([t for t in tasks if t['completed']])
    pending = len([t for t in tasks if not t['completed']])
    now = datetime.now()
    overdue = len([
        t for t in tasks
        if t['due_date'] and datetime.strptime(t['due_date'], '%Y-%m-%d') < now and not t['completed']
    ])
    return jsonify({
        'total_tasks': total,
        'completed': completed,
        'pending': pending,
        'overdue': overdue
    })


if __name__ == '__main__':
    # server will run on port 5000
    app.run(host='0.0.0.0', port=5000, debug=True)
