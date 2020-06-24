from flask import flash, redirect
from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, BooleanField, SubmitField, PasswordField, RadioField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Please enter user name')])
    password = PasswordField('Password', validators=[DataRequired(message='Please enter password')])
    remember_me = BooleanField('Remember Me')
    sign_in = SubmitField('Sign In')
    forgot_password = SubmitField('Forgot Password')

class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(message='Please enter user name')])
    password = PasswordField('Password', validators=[DataRequired(message='Please enter password')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(message='Please re-enter password')])
    email = StringField('e-mail address', validators=[DataRequired(message='Please enter password')])
    register = SubmitField('Register')

