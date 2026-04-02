from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, IntegerField
from wtforms.validators import DataRequired, NumberRange

class StudentForm(FlaskForm):
    name = StringField('Enter Name:',validators=[DataRequired()])
    science1 = SelectField('Select a Science', choices=[('None', 'None'),('CS', 'Computer Science'), ('BIO', 'Biology'), ('CHEM', 'Chemistry')])
    science2 = SelectField('Select a Science', choices=[('None', 'None'),('CS', 'Computer Science'), ('BIO', 'Biology'), ('CHEM', 'Chemistry')])
    science3 = SelectField('Select a Science', choices=[('None', 'None'),('CS', 'Computer Science'), ('BIO', 'Biology'), ('CHEM', 'Chemistry')])
    submit = SubmitField('Submit')

class GenerateGroupsForm(FlaskForm):
    num_groups = IntegerField('Enter Number of Groups:', default=2 ,validators=[DataRequired(),NumberRange(min=2, max=10)])
    generate = SubmitField('Generate')
    submit = SubmitField('submit')