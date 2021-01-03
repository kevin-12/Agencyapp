from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from flask_wtf import FlaskForm,form,Form,RecaptchaField
from werkzeug.security import check_password_hash,generate_password_hash
from passlib.hash import pbkdf2_sha256
from wtforms import Form, StringField,PasswordField,SubmitField,validators,BooleanField,DateField,RadioField
from wtforms.validators import InputRequired,Length,EqualTo,ValidationError
from .model import *
from flask_wtf.file import FileField, FileAllowed, FileRequired


def invalid_credentials(form,field):

  """username and password checker"""
  username_entered=form.Username.data
  password=field.data

  #check user name is invalid
  user_object=User.query.filter_by(Username=username_entered).first() 
  if user_object is None:
     raise ValidationError("Username or password is incorrect")
  #check if password is invalid
  elif not pbkdf2_sha256.verify(password, user_object.password):
    raise ValidationError("Username or password is incorrect")



class RegistrationForm(Form):

    ''' Registration form'''
    Username = StringField('Username', [validators.Length(min=4, max=25)])
    email = StringField('Email Address', [validators.Length(min=6, max=35)])
    password = PasswordField('New Password', [
    validators.DataRequired(),
    validators.EqualTo('confirm', message='Passwords must match') ])
    confirm = PasswordField('Repeat Password')
    accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
  
class LoginForm(Form):
  """login form"""
  Username = StringField(validators=[InputRequired(message="Username required")])
  password=PasswordField(validators=[InputRequired(message='Password required'),invalid_credentials])
  submit_button=SubmitField('Login')


class NannyApplicationForm(Form):

  """nannies"""
  name=StringField('Name', [validators.Length(min=1, max=25)])
  username = StringField('Username', [validators.Length(min=4, max=25)])
  email = StringField('Email Address', [validators.Length(min=6, max=35)])
  password = PasswordField('New Password', [
  validators.DataRequired(),
  validators.EqualTo('confirm', message='Passwords must match') ])
  confirm = PasswordField('Repeat Password')
  city = StringField('City', [validators.Length(min=1, max=35)])
  curriculum = FileField([validators.DataRequired()])
  accept_tos = BooleanField('I accept the TOS', [validators.DataRequired()])
  
class Book(Form):
  """Searchform"""
  city= StringField('City',[validators.Length(min=1, max=25)])
  
  
