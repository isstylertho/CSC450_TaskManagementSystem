from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, DateField, TimeField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, EqualTo, Length

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired()])

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(max=150)])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=8)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])

class TaskForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired(), Length(max=150)])
    description = TextAreaField('Description', validators=[Length(max=500)])
    date = DateField('Date', validators=[DataRequired()], format='%Y-%m-%d')
    time = TimeField('Time', validators=[DataRequired()], format='%H:%M')
    completed = BooleanField('Completed')
    submit = SubmitField('Save Task')
