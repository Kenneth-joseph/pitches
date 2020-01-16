from flask_wtf import FlaskForm
from wtforms import StringField,SelectField,TextAreaField,SubmitField,TimeField,PasswordField,BooleanField
from wtforms.validators import Required,EqualTo
from wtforms import ValidationError
from ..models import User

class UserRegistration(FlaskForm):
    email=StringField('Your Email Address', validators=[Required()])
    username = StringField('Enter your username',validators = [Required()])
    password = PasswordField('Password',validators = [Required(), EqualTo('password_confirm',message = 'Passwords must match')])
    password_confirm = PasswordField('Confirm Passwords',validators = [Required()])
    submit = SubmitField('Sign Up')

class LoginForm(FlaskForm):
    username = StringField('Username',validators=[Required()])
    password  = PasswordField('Password',validators=[Required()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


    def validate_email(self,data_field):
         if User.query.filter_by(email =data_field.data).first():
                raise ValidationError('There is an account with that email')
 
    
    def validate_username(self,data_field):
        if User.query.filter_by(name= data_field.data).first():
            raise ValidationError("Username already exists")
