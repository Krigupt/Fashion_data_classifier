from flask_wtf import FlaskForm
from wtforms import StringField,PasswordField,SubmitField,BooleanField,SelectField
from wtforms.validators import DataRequired,Length,EqualTo,ValidationError
from fashion_classifier.models import User,ClothingData
from flask_wtf.file import FileField, FileAllowed


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm_Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('That email is taken. Please choose a different one.')




class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')


class Classify(FlaskForm):
    cloth_types = SelectField('categories', choices=[('T-SHIRT'),('SHIRT'),('PANTS'),('SHORTS'),('JACKETS'),('HATS/CAPS')])
    gender_types = SelectField('categories',
                              choices=[('MALE'), ('FEMALE'), ('BINARY'),])
    size_types = SelectField('categories',
                              choices=[ ('XS'),('S'), ('L'), ('XL'), ('XXL'), ('XXXL')])
    color = StringField('Color', validators=[DataRequired()])
    image_file = FileField('Choose a picture from the directory', validators=[FileAllowed(['jpg','png','jpeg'])])

    def validate_username(self,picture ):
        user = User.query.filter_by(image_file=picture.data).first()
        if user:
            raise ValidationError('That picture is taken. Please choose a different one.')








