from flask import Flask, flash, jsonify, redirect, request, abort, render_template, url_for
from flask_sqlalchemy import SQLAlchemy
import os
from datetime import datetime
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

#app = Flask(__name__) 
app = Flask(__name__, 
    template_folder=os.path.join(os.path.dirname(__file__), '..', '..', 'templates'), #this resolves templates Jinja error
    static_folder=os.path.join(os.path.dirname(__file__), '..', '..', 'static') #have to specify static folder path since we are specifying template location
)

# Configure MySQL database connection
app.config['SQLALCHEMY_DATABASE_URI'] = (f"mysql+mysqlconnector://{os.getenv('MYSQL_USER')}:{os.getenv('MYSQL_PASSWORD')}@"f"{os.getenv('MYSQL_HOST')}/{os.getenv('MYSQL_DATABASE')}")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Check if the variables are loaded correctly
print(os.getenv('MYSQL_USER'))  # Should print 'root'
print(os.getenv('MYSQL_PASSWORD'))  # Should print the password
print(os.getenv('MYSQL_HOST'))  # Should print '34.148.30.117'
print(os.getenv('MYSQL_DATABASE'))  # Should print 'CSC450TaskManagement'

db = SQLAlchemy(app)

with app.app_context():
    db.create_all()

#this function handles updating the calendar integration link to the database
# @app.route('/calendar-view.html/submit', methods=['POST'])
# def updateCalendarLink():
#     user_input = request.form['user_input']  # gets the value from the form input
#     #update database
#     connection = get_db_connection() #calls whatever function connects to the database
#     try:
#         with connection.cursor() as cursor:
#             cursor.execute("UPDATE user SET calendarLink = %s WHERE id = 1;", (user_input,))  # Passing the user input string safely as a tuple - the comma is required to be considered a tuple
#     finally:
#         connection.close() #close connection to database
#     return "You have succesfully updated your calendar link."
    
@app.route("/overview.html") #ensures function returns to correct html
def taskOverview():
    return render_template('overview.html')

@app.route("/completed-tasks.html") #ensures function returns to correct html
def completedTasks():
    return render_template('completed-tasks.html')

@app.route("/today.html") #ensures function returns to correct html
def today():
    return render_template('today.html')

@app.route("/calendar-view.html") #ensures function returns to correct html
def calendarview():
    # connection = get_db_connection() #calls whatever function connects to the database
    # try:
    #     with connection.cursor() as cursor:
    #         cursor.execute("SELECT calendarLink FROM user WHERE;") #correct IDs if incorrect, add ~"WHERE (SELECT username FROM user)== current_user" to ensure we are calling the active user's calendar link. Could the current_user username be pulled from the login function?
    #         data = cursor.fetchall()
    # finally:
    #     connection.close() #close connection to database

    #example link to ensure displaying works correctly
    exampledata = "https://calendar.google.com/calendar/embed?src=99e4a12c367f46da20767ad231758801f88590a44d364cb032aeab6c0df5b5d0%40group.calendar.google.com&ctz=America%2FNew_York" #TEST

    #return render_template('calendar-view.html', data=data) #returns user's URL link for calendar pulled from DB
    return render_template('calendar-view.html', exampledata=exampledata) #TEST: returns user's URL link for calendar from variable

@app.route("/user-interface.html")
def userinterface():
    return render_template("user-interface.html")

# Models
class User(db.Model):
    __tablename__ = 'Users'
    UserID = db.Column(db.Integer, primary_key=True)
    Username = db.Column(db.String(50), nullable=False)
    Email = db.Column(db.String(100), nullable=False, unique=True)
    Password = db.Column(db.String(255), nullable=False)
    UserTasks = db.Column(db.String(255))  # Can be normalized if required

    def __repr__(self):
        return f"<User {self.UserID}, {self.Username}, {self.Email}>"

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
    UserID = db.Column(db.Integer, db.ForeignKey('Users.UserID', ondelete='CASCADE'))
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
    return jsonify([{'UserID': user.UserID, 'Username': user.Username, 'Email': user.Email} for user in users])

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

# Error handlers
@app.errorhandler(400)
def bad_request(error):
    return jsonify({'error': 'Bad Request', 'message': error.description}), 400

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not Found', 'message': error.description}), 404


if __name__ == '__main__':
    app.run(debug=True, port=5001) #added a different port in case something on PC is already using 5000