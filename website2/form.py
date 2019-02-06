# forms.py

from wtforms import Form, StringField, SelectField, validators

class KinaseForm(Form):
    search = StringField('')
