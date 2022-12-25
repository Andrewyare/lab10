from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField, SelectField, TextAreaField
from wtforms.validators import DataRequired, Email, Length, Regexp


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
