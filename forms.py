from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.fields import PasswordField, BooleanField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from models import User


class UserLoginForm(FlaskForm):
    """For the user to log in"""
    username = StringField('Username', validators=[DataRequired(message='Please fill in your username.')],
                           description={'placeholder': 'Username'})
    password = PasswordField('Password', validators=[DataRequired(message='Please enter your password.')],
                             description={'placeholder': 'Password'}, render_kw={'autocomplete': 'on'})
    remember = BooleanField('Remember me', default=False, description={'loc': 'footer'})
    submit = SubmitField('Sign in', description={'loc': 'footer'})

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is None:
            raise ValidationError("An account with this username doesn't exist.")

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user is not None and not user.check_password(password.data):
            raise ValidationError("The username or password is incorrect.")


class UserRegistrationForm(FlaskForm):
    """For the user to register"""
    name = StringField('First Name', validators=[DataRequired(message='Enter your full name.')], )
    surname = StringField('Surname', validators=[DataRequired(message='Enter your surname.')], )
    username = StringField('Username', validators=[DataRequired(message='Enter a username.')])
    email = StringField('Email', validators=[Email(message='Not a valid email address.'),
                                             DataRequired(message="Please enter an email address.")])
    password = PasswordField('Password',
                             validators=[Length(min=5, max=20,
                                                message='Your password should be between 5 and 20 characters.'),
                                         DataRequired()],
                             render_kw={'autocomplete': 'on'})
    confirm_password = PasswordField('Repeat Password',
                                     validators=[DataRequired(),
                                                 EqualTo('password', message='Passwords must match.')],
                                     render_kw={'autocomplete': 'on'})
    agree = BooleanField(validators=[DataRequired(message="Indicate that you agree with the terms and conditions.")],
                         description={'loc': 'footer'})
    submit = SubmitField('Register', description={'loc': 'footer'})

    @staticmethod
    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('This username is taken.')

    @staticmethod
    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('An account already exisits with this email.')
