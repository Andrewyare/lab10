from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField, SelectField, TextAreaField, PasswordField, BooleanField ,validators,ValidationError
from wtforms.validators import DataRequired, Email, Length, Regexp

from .models import User

class ContactForm(FlaskForm):
    name = StringField("Name", 
                      [DataRequired("Please enter your name."), 
                       Length(min=4, max=10, message ='Length must be between 4 and 10')
                       ])
    email = StringField('Email', validators=[Email("Please enter correct email")])
    phone = StringField('Phone',
    validators=[Regexp('(^380\s?[0-9]{2}\s?[0-9]{3}\s?[0-9]{4}$)$', message='Enter correct number')])
    subject = SelectField('Subject', choices=['Football', 'Basketball', 'Golf', 'Voleyball'])
    message = TextAreaField('Message', validators=[DataRequired("Enter a message."), Length(min=0,max=500)])
    submit = SubmitField("Send")

class RegistrationForm(FlaskForm):
	name = StringField("Name", 
	                  [
						DataRequired("Please enter your name."), 
					    Regexp('^[A-Za-z][a-zA-Z0-9_.-]+$', message='Name must have only letters, numbers, dots or underscores.'),
	                    Length(min=4, max=10, message ='Length must be between 4 and 10')
	                   ])
	email = StringField('Email', validators=[Email("Please enter correct email")])
	password = PasswordField('Password', [
        validators.DataRequired(),
        validators.EqualTo('password_confirm', message='Passwords must match')
    ])
	password_confirm = PasswordField('Repeat Password')
	submit = SubmitField("Send")

	def validate_email(self, field):
		if User.query.filter_by(email=field.data).first():
			raise ValidationError('Email already registered.')

	def validate_name(self,field):
		if User.query.filter_by(name=field.data).first():
			raise ValidationError('Name already taken.')

class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember me')
	submit = SubmitField('Login')

	