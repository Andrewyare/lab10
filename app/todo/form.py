from flask_wtf import FlaskForm  
from wtforms import StringField, SubmitField, SelectField, DateField
from wtforms.validators import DataRequired, Length, Email
from flask_ckeditor import CKEditorField
from .models import Category


def get_category_list():
    return [(cat.id, cat.name) for cat in Category.query.all()]

class Taskform(FlaskForm):

    title = StringField("Title",
                        [DataRequired("Please enter task title."),
                         Length(min=4, max=100, message='Це поле має бути довжиною між 4 та 10 символів')
                         ])
    description = CKEditorField('Description',
                                validators=[Length(max=2048, message='Це поле має бути довжиною до 2048 символів')])
    deadline = DateField('Deadline')
    priority = SelectField('Priority', choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')])
    progress = SelectField('Progress', choices=[(1, 'Todo'), (2, 'Doing'), (3, 'Done')])
    category = SelectField("Category")
    submit = SubmitField("Send")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.category.choices = get_category_list()

class CategoryForm(FlaskForm):
    name = StringField('Name', [DataRequired()])
    submit = SubmitField('Submit')

class AssignUserForm(FlaskForm):
    email = StringField("Email",
                       [DataRequired(), Email()])
    submit = SubmitField("Send")

