from flask import Flask, jsonify, request, abort
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.id}, {self.title}, {self.completed}>"

with app.app_context():
    db.create_all()

# Route to get all tasks
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([{'id': task.id, 'title': task.title, 'completed': task.completed} for task in tasks])

# Route to create a new task
@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()

    if not data or 'title' not in data:
        abort(400, description= "Missing title in the request")

    new_task = Task(title=data['title'])
    db.session.add(new_task)
    db.session.commit()

    return jsonify({'id': new_task.id, 'title': new_task.title, 'completed': new_task.completed}), 201

# Route to update a task's completion status
@app.route('/tasks/<int:id>', methods=['PATCH'])
def update_task(id):
    task = Task.query.get(id)
    if not task:
        abort(404, description="Task not found")

    data = request.get_json()
    if 'completed' in data:
        task.completed = data['completed']
        db.session.commit()

    return jsonify({'id': task.id, 'title': task.title, 'completed': task.completed})

# Route to delete a task
@app.route('/tasks/<int:id>', methods=['DELETE'])
def delete_task(id):
    task = Task.query.get(id)
    if not task:
        abort(404, description="Task not found")

    db.session.delete(task)
    db.session.commit()

    return jsonify({'message': 'Task deleted successfully'})

# Error handler for bad requests
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

# Error handler for not found tasks
@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': error.description}), 404

if __name__ == '__main__':
    app.run()
