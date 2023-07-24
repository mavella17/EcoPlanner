from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms import BooleanField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, ValidationError
from wtforms.validators import EqualTo, InputRequired, NumberRange
import airportsdata


# create a class to encapsulate data from the drive form
class driveData(FlaskForm):
    vehiclemodel = StringField('Vehicle Model', validators=[InputRequired()])
    # TODO: add a feature where distance can be change from miles to kilometers
    distance = IntegerField('Distance', validators=[DataRequired()])
    distance_type = SelectField('Miles or Kilometers',
                                choices=[('mi', 'Miles'),
                                         ('km', 'Kilometers')])
    submit = SubmitField('Calculate Emissions')


# create a class to encapsulate data from the flights form
class flightData(FlaskForm):
    
    def validate_code(form, field):
        airports = airportsdata.load('IATA').keys()
        if field.data.upper() not in airports:
            raise ValidationError('Not a valid code')
   
    wherefrom = StringField('Where From?',
                            validators=[DataRequired(), Length(min=1, max=3),
                                        validate_code])
    whereto = StringField('Where To?',
                          validators=[DataRequired(), Length(min=1, max=3),
                                      validate_code])
    passengers = IntegerField('Number of Passengers',
                          validators=[DataRequired(),NumberRange(min=1, max=10)])
    submit = SubmitField('Calculate Emissions')


# Created the register class where users can register
class registrationData(FlaskForm):
    username = StringField('Username',
                           validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up!')
