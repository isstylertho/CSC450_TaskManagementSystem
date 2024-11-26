from flask import Flask, flash, jsonify, redirect, request, abort, render_template, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
#from application.src.forms import LoginForm, RegistrationForm, TaskForm
import os
from datetime import datetime
from dotenv import load_dotenv
import validators

# Load environment variables
load_dotenv()

#app = Flask(__name__) 
app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(__file__), '..', '..', 'templates'), #this resolves templates Jinja error
    static_folder=os.path.join(os.path.dirname(__file__), '..', '..', 'static') #have to specify static folder path since we are specifying template location
)

# Set the secret key for the app to handle sessions securely
app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY', 'your_default_secret_key')

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Check if the variables are loaded correctly
print(os.getenv('MYSQL_USER'))  # Should print 'root'
print(os.getenv('MYSQL_PASSWORD'))  # Should print the password
print(os.getenv('MYSQL_HOST'))  # Should print '34.148.30.117'
print(os.getenv('MYSQL_DATABASE'))  # Should print 'CSC450TaskManagement'

db = SQLAlchemy(app)

# Initialize LoginManager
login_manager = LoginManager(app)  # Initialize the login manager with the Flask app
login_manager.login_view = 'login'  # Specify the login route for redirection

with app.app_context():
    db.create_all()

# Checks if user is logged in
# @app.route('/')
# def index():
#     if current_user.is_authenticated:
#         return redirect(url_for('main.dashboard')) #direct to overview
#     return render_template('login.html') #directs user to log in if not already

# Load user function for Flask-Login
@login_manager.user_loader
def load_user(user_id):
    return User.query.filter_by(UserID=user_id).first()

# This restores session['userID'] from current_user after a restart
@app.before_request
def sync_session_with_user():
    if current_user.is_authenticated and not session.get('userID'):
        session['userID'] = current_user.get_id()
        print(f"Session restored: {session['userID']}")

        # Debugging session and current_user
        print(f"Session userID: {session.get('userID')}")
        print(f"Current user authenticated: {current_user.is_authenticated}")
        print(f"Current user ID: {current_user.get_id() if current_user.is_authenticated else None}")

# User authentication routes
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # If the user is already logged in
        return redirect(url_for('taskOverview'))
    
    if request.method == 'POST':
        user_id = request.form.get('userID')
        password = request.form.get('password')

        if not user_id or not password:
            return render_template('login.html', error="Missing userID or password")

        user = User.query.filter_by(UserID=user_id).first()
        if user and check_password_hash(user.Password, password):
            login_user(user)
            session['userID'] = user.UserID  # Store userID in session
            return redirect(url_for('calendarView'))
        elif user and not check_password_hash(user.Password, password):
            print("Password entered is incorrect")
            return render_template('login.html', error="Invalid userID or password")
        elif not user:
            print("User does not exist, please register")
            return render_template('register.html', error="Invalid userID or password")
        else:
            print("error: something funky is happening, try again")
            return render_template('login.html', error="Invalid userID or password")
            
    return render_template('login.html')

# New user registration
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form.get('email')
        user_id = request.form.get('userID')
        password = request.form.get('password')
        
        user_id = request.form.get('userID')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Validate input
        if not user_id or not email or not password:
            print('invalid input')
            return render_template('register.html', error="Missing fields")
        
        # Hash the password before storing it
        hashed_password = generate_password_hash(password, method='pbkdf2:sha256')

        # Check if the user already exists
        existing_user = User.query.filter_by(UserID=user_id).first()
        if existing_user:
            print('An account is already associated with that username. Please sign in or try again.')
            return redirect(url_for('login'))

        # Create new user and store in DB
        new_user = User(UserID=user_id, Email=email, Password=hashed_password)  # Using email as UserID
        db.session.add(new_user)
        db.session.commit()

        #flash('Registration successful! Please log in.', 'success')
        print('registration successful - please log in')
        return redirect(url_for('login'))  # Redirect to login after registration

    print('form not working')
    return render_template('register.html')

@app.route('/logout', methods=['GET', 'POST'])
@login_required
def logout():
    logout_user()
    return redirect(url_for('login')) #redirects user to login.html when user is logged out

@app.route("/calendar-view.html")
@login_required
def calendarView():
    # Get userID from session
    user_id = session.get('userID')
    if not user_id:
        flash("You need to log in first.", "error")
        return redirect(url_for('login'))

    # Fetch user from database
    user = User.query.filter_by(UserID=user_id).first()
    if not user:
        flash("User not found. Please log in again.", "error")
        return redirect(url_for('login'))

    # Render calendar view
    if user:
        # Validate calendarURL
        if user.calendarURL and validators.url(user.calendarURL):
            return render_template('calendar-view.html', data=user.calendarURL)
        else:
            flash("Invalid calendar link. Please update your settings.", "error")
            return render_template('calendar-view.html', data=None)
    else:
        flash("Your calendar link is not set. Please update it in settings.", "error")
        print("Your calendar link is not set. Please update it in settings.")
        return render_template('calendar-view.html', data=None)


@app.route("/overview.html") #ensures function returns to correct html
@login_required
def taskOverview():
    return render_template('overview.html')

@app.route("/completed-tasks.html") #ensures function returns to correct html
@login_required
def completedTasks():
    return render_template('completed-tasks.html')

@app.route("/today.html") #ensures function returns to correct html
@login_required
def today():
    return render_template('today.html')

@app.route("/user-interface.html")
@login_required
def userinterface():
    return render_template("user-interface.html")

# Models
class User(UserMixin, db.Model): #UserMixin allows check for active user
    __tablename__ = 'Users'
    UserID = db.Column(db.String(50), primary_key=True) #removed username field - this will be the username
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    calendarURL = db.Column(db.String(255), nullable=True)
    UserTasks = db.Column(db.String(255))  # Can be normalized if required

    def __repr__(self):
        return f"<User {self.UserID}, {self.Email}>"
    
    @property
    def is_active(self):
        # prevents - AttributeError: 'User' object has no attribute 'is_active'
        return True
    
    def get_id(self):
        return self.UserID  # Returns unique identifier of the user

class Task(db.Model):
    __tablename__ = 'Tasks'
    TaskID = db.Column(db.Integer, primary_key=True)
    TaskName = db.Column(db.String(100), nullable=False)
    Description = db.Column(db.Text)
    Priority = db.Column(db.Integer)  # 1=High, 2=Medium, 3=Low
    CreationDate = db.Column(db.Date, nullable=False, default=datetime.utcnow)
    DueDate = db.Column(db.Date)

    def __repr__(self):
        return f"<Task {self.TaskID}, {self.TaskName}, Priority: {self.Priority}>"

class List(db.Model):
    __tablename__ = 'Lists'
    ProjectID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.String(50), db.ForeignKey('Users.UserID', ondelete='CASCADE'))
    TaskID = db.Column(db.Integer, db.ForeignKey('Tasks.TaskID', ondelete='SET NULL'))
    ListName = db.Column(db.String(100), nullable=False)
    ListDescription = db.Column(db.Text)

    def __repr__(self):
        return f"<List {self.ProjectID}, {self.ListName}>"

class Comment(db.Model):
    __tablename__ = 'Comments'
    CommentID = db.Column(db.Integer, primary_key=True)
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID', ondelete='CASCADE'))
    TaskID = db.Column(db.Integer, db.ForeignKey('Tasks.TaskID', ondelete='SET NULL'))
    Content = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<Comment {self.CommentID}, User {self.UserID}, Task {self.TaskID}>"

# Ensure database tables are created
with app.app_context():
    db.create_all()

# Routes

# Users Endpoints
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([{'UserID': user.UserID, 'Email': user.Email} for user in users])

@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'Username' not in data or 'Email' not in data or 'Password' not in data:
        abort(400, description="Missing required fields")
    
    new_user = User(Username=data['Username'], Email=data['Email'], Password=data['Password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({'UserID': new_user.UserID, 'Username': new_user.Username, 'Email': new_user.Email}), 201

@app.route('/users/<int:UserID>', methods=['DELETE'])
def delete_user(UserID):
    user = User.query.get(UserID)
    if not user:
        abort(404, description="User not found")
    
    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})

# Tasks Endpoints
@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all()
    return jsonify([
        {'TaskID': task.TaskID, 'TaskName': task.TaskName, 'Priority': task.Priority, 
         'CreationDate': task.CreationDate, 'DueDate': task.DueDate}
        for task in tasks
    ])

@app.route('/tasks', methods=['POST'])
def create_task():
    data = request.get_json()
    if not data or 'TaskName' not in data or 'Priority' not in data or 'CreationDate' not in data:
        abort(400, description="Missing required fields")
    
    new_task = Task(
        TaskName=data['TaskName'], 
        Description=data.get('Description'), 
        Priority=data['Priority'], 
        CreationDate=data['CreationDate'], 
        DueDate=data.get('DueDate')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({'TaskID': new_task.TaskID, 'TaskName': new_task.TaskName}), 201

@app.route('/tasks/<int:TaskID>', methods=['DELETE'])
def delete_task(TaskID):
    task = Task.query.get(TaskID)
    if not task:
        abort(404, description="Task not found")
    
    db.session.delete(task)
    db.session.commit()
    return jsonify({'message': 'Task deleted successfully'})

# Comments Endpoints
@app.route('/comments', methods=['GET'])
def get_comments():
    comments = Comment.query.all()
    return jsonify([
        {'CommentID': comment.CommentID, 'UserID': comment.UserID, 'TaskID': comment.TaskID, 'Content': comment.Content}
        for comment in comments
    ])

@app.route('/comments', methods=['POST'])
def create_comment():
    data = request.get_json()
    if not data or 'UserID' not in data or 'TaskID' not in data or 'Content' not in data:
        abort(400, description="Missing required fields")
    
    new_comment = Comment(UserID=data['UserID'], TaskID=data['TaskID'], Content=data['Content'])
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'CommentID': new_comment.CommentID, 'Content': new_comment.Content}), 201

#this function handles updating the calendar integration link to the database
@app.route('/calendar-view.html/submit', methods=['POST'])
def updateCalendarURL():
    user_input = request.form.get('user_input')  # Get value from the form input

    user_id = session.get('userID')  # Get userID from session
    if not user_id:
        print('User not found: if not user_id')
        return redirect(url_for('login'))

    # Query the user by userID matching the current session
    user = User.query.filter_by(UserID=user_id).first()
    if user:
        # Update the calendarURL
        user.calendarURL = user_input
        db.session.commit()  # Commit the change to the database
        print("You have successfully updated your calendar link.")
        flash("Calendar link updated successfully!", "success")
        return redirect(url_for('calendarView'))
    else:
        print('Calendar URL failed to update')
        flash("Failed to update the calendar link. Please try again.", "error")
        return redirect(url_for('calendarView'))


# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': error.description}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001) #added a different port in case something on PC is already using 5000
