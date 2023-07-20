from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, IntegerField, SelectField, RadioField
from wtforms.validators import DataRequired, Length, Email, EqualTo, InputRequired

#create a class to encapsulate data from the drive form 
class driveData(FlaskForm):
   #TODO: need to change the vehiclemodel paramter to match what is required by the API
   vehiclemodel = StringField('Vehicle Model', validators=[InputRequired()])
   #TODO: add a feature where distance can be change from miles to kilometers
   distance = IntegerField('Distance', validators=[DataRequired()])
   distance_type = SelectField('Miles or Kilometers', choices=[('mi', 'Miles'), ('km', 'Kilometers')])
   submit = SubmitField('Calculate Emissions')

#create a class to encapsulate data from the flights form
class flightData(FlaskForm):
    wherefrom = StringField('Where From?', validators=[DataRequired(), Length(min=1, max=20)])
    whereto = StringField('Where To?', validators=[DataRequired(), Length(min=1, max=20)])
    submit = SubmitField('Calculate Emissions') 