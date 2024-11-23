from flask import Blueprint, Flask, render_template, redirect, url_for, request, jsonify, flash
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.forms import LoginForm, RegistrationForm, TaskForm
from app.models import User, Task, db

app = Flask(__name__)

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

# Set the login view (where to redirect if the user isn't logged in)
login_manager.login_view = 'login'

@app.route('/')
def index():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    return render_template('login.html')

# User authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and check_password_hash(user.password, form.password.data):
            login_user(user)
            return redirect(url_for('dashboard'))
        flash('Invalid username or password.')
    return render_template('login.html', form=form)

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

# Task management routes
@app.route('/dashboard', methods=['GET', 'POST'])
@login_required
def dashboard():
    form = TaskForm()
    if form.validate_on_submit():
        task = Task(
            title=form.title.data,
            description=form.description.data,
            date=form.date.data,
            time=form.time.data,
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        flash('Task added successfully!')
        return redirect(url_for('dashboard'))
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    return render_template('tasks/dashboard.html', form=form, tasks=tasks)

@app.route('/tasks', methods=['GET'])
@login_required
def get_tasks():
    tasks = Task.query.filter_by(user_id=current_user.id).all()
    events = [
        {
            'id': task.id,
            'title': task.title,
            'start': f"{task.date}T{task.time}",
            'completed': task.completed
        } for task in tasks
    ]
    return jsonify(events)

@app.route('/task', methods=['POST', 'PUT'])
@login_required
def update_task():
    task_data = request.get_json()
    if request.method == 'POST':
        task = Task(
            title=task_data['title'],
            description=task_data['description'],
            date=task_data['date'],
            time=task_data['time'],
            completed=task_data['completed'],
            user_id=current_user.id
        )
        db.session.add(task)
        db.session.commit()
        return jsonify({"status": "success", "message": "Task created successfully!"})
    elif request.method == 'PUT':
        task = Task.query.get_or_404(task_data['id'])
        task.title = task_data['title']
        task.description = task_data['description']
        task.date = task_data['date']
        task.time = task_data['time']
        task.completed = task_data['completed']
        db.session.commit()
        return jsonify({"status": "success", "message": "Task updated successfully!"})

@app.route('/task/<int:task_id>', methods=['DELETE'])
@login_required
def delete_task(task_id):
    task = Task.query.get_or_404(task_id)
    db.session.delete(task)
    db.session.commit()
    return jsonify({"status": "success", "message": "Task deleted successfully!"})

#runs the app
if __name__ == '__main__':
    # This line ensures the app listens on all network interfaces (0.0.0.0) and runs on port 5000 as specified in the docker-compose.yml file
    app.run(host='0.0.0.0', port=5000, debug=True)