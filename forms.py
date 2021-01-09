from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField
from wtforms.validators import DataRequired, NumberRange, Optional

from datetime import datetime


class StudentAddForm(FlaskForm):
    first_name = TextField("First Name", validators=[DataRequired()])
    last_name = TextField("Last Name", validators=[DataRequired()])
    email = TextField("Email", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])

class ProblemAddForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])
    build = StringField("Build", validators=[DataRequired()])


class ProblemEditForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", validators=[DataRequired()])

    
