from flask import render_template,redirect,url_for,request,flash
from ..models import User
from .form import UserRegistration,LoginForm
from .. import db
from . import auth
from flask_login  import login_user,login_required,logout_user
# from ..email import mail_message


@auth.route('/register',methods = ["GET","POST"])
def register():
    form=UserRegistration()
    if form.validate_on_submit():
        user=User(email=form.email.data, name=form.username.data,password=form.password.data)
        user.save_user()
        # mail_message("Welcome to Pitch friend","email/welcome_user", user.email,user=user)
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)


@auth.route('/login',methods = ["GET","POST"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(name =form.username.data).first()
        if user != None and user.verify_password(form.password.data):
            login_user(user,form.remember.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid Username or password')  
    return render_template('auth/login.html',loginform=form)    


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for("main.index"))

