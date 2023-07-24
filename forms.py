from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import BooleanField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email
from wtforms.validators import EqualTo, InputRequired, NumberRange


# create a class to encapsulate data from the drive form
class driveData(FlaskForm):
    vehiclemodel = StringField('Vehicle Model', validators=[InputRequired()])
    # TODO: add a feature where distance can be change from miles to kilometers
    distance = IntegerField('Distance', validators=[DataRequired(), NumberRange(min=0, max=10)])
    distance_type = SelectField('Miles or Kilometers',
                                choices=[('mi', 'Miles'),
                                         ('km', 'Kilometers')])
    submit = SubmitField('Calculate Emissions')


# create a class to encapsulate data from the flights form
class flightData(FlaskForm):
    wherefrom = StringField('Where From?',
                            validators=[DataRequired(), Length(min=1, max=4)])
    whereto = StringField('Where To?',
                          validators=[DataRequired(), Length(min=1, max=4)])
    passengers = IntegerField("Passengers:",
                          validators=[DataRequired()])
    submit = SubmitField('Calculate Emissions')


# Created the register class where users can register
class registrationData(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField(validators=[DataRequired()])
    submit = SubmitField('Sign Up!')
    