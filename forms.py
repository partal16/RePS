from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, RadioField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional
from wtforms.widgets import TextArea


class ProblemAddForm(FlaskForm):
    builds = [('School of Foreign Languages Building (DIB)','School of Foreign Languages Building (DIB)'),
              ('Electrics and Electronics Building (EEB)', 'Electrics and Electronics Building (EEB)'),
              ('Faculty of Science and Literature Building (FEB)','Faculty of Science and Literature Building (FEB)'),
              ('Naval Architecture and Ocean Engineering Building (GDB)', 'Naval Architecture and Ocean Engineering Building (GDB)'),
              ('Olympic Pool (HVZ)', 'Olympic Pool (HVZ)'),
              ('Civil Building (INB)', 'Civil Building (INB)'),
              ('Management Building (ISB)', 'Management Building (ISB)'),
              ('Social and Cultural Area Building (KSB)', 'Social and Cultural Area Building (KSB)'),
              ('Chemistry and Metallurgy Building (KMB)', 'Chemistry and Metallurgy Building (KMB)'),
              ('Lecture Hall A Building (MED)', 'Lecture Hall A Building (MED)'),
              ('Gölet Derslik Building (MEDB)', 'Gölet Derslik Building (MEDB)'),
              ('Mines Building (MDB)', 'Mines Building (MDB)'),
              ('Mechanical Building (MKB)', 'Mechanical Building (MKB)'),
              ('Architecture Building (MMB)', 'Architecture Building (MMB)'),
              ('Süleyman Demirel Cultural Center (SDKM)', 'Süleyman Demirel Cultural Center (SDKM)'),
              ('Sport Center (SMB)', 'Sport Center (SMB)'),
              ('Healty Life Center (SYM)', 'Healty Life Center (SYM)'),
              ('Aeronautics and Astronautics Building (UUB)', 'Aeronautics and Astronautics Building (UUB)'),
              ('Construction and Earthquake Building (YDB)', 'Construction and Earthquake Building (YDB)'),
              ('75th Year Student Social Center Dinning Hall', '75th Year Student Social Center Dinning Hall'),
              ('Mustafa Inan Library', 'Mustafa Inan Library'),
              ]
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", widget=TextArea())
    build = SelectField("Build", choices=builds)
    solution_r = StringField("Solution_R", widget=TextArea())
    privacy = RadioField("Privacy", choices=[(False,'Private'), (True, 'Public')])


class ProblemEditForm(FlaskForm):
    title = StringField("Title", validators=[DataRequired()])
    description = StringField("Description", widget=TextArea())
    solution_r = StringField("Solution_R", widget=TextArea())

    
