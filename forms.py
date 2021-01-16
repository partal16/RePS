from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, RadioField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms.widgets import TextArea
from datetime import datetime


class ProblemAddForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", widget=TextArea())
    build = StringField("Build", validators=[DataRequired()])
    solution_r = StringField("Solution_R", widget=TextArea())
    privacy = RadioField("Privacy", choices=[(False,'Private'), (True, 'Public')])


class ProblemEditForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", widget=TextArea())
    solution_r = StringField("Solution_R", widget=TextArea())

    
