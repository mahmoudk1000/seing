from sqlalchemy.orm import validates
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, RadioField, EmailField, PasswordField, TextAreaField, BooleanField
from wtforms.validators import DataRequired, Length


class SearchForm(FlaskForm):
    toggle = BooleanField('Net Search')
    query = StringField('q', validators=[DataRequired(), Length(1, 64)], render_kw={'autocomplete': 'off'})
    submit = SubmitField('submit')


class WebDataForm(FlaskForm):
    web_list = TextAreaField('Enter comma-seperated List or Query: ', validators=[DataRequired()])
    web_type = RadioField('Select Type: ', choices=[('list', 'List'), ('query', 'Query')], validators=[DataRequired()])
    submit = SubmitField('submit')


class LoginForm(FlaskForm):
    email = EmailField('Email:', validators=[DataRequired(), Length(10, 64)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(8, 32)])
    login = SubmitField('Login')


class RegisterForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(6, 24)])
    email = EmailField('Email:', validators=[DataRequired(), Length(10, 64)])
    password = PasswordField('Password:', validators=[DataRequired(), Length(8, 32)])
    conf_password = PasswordField('Confirm Password:', validators=[DataRequired(), Length(8, 32)])
    register = SubmitField('Sign Up')
