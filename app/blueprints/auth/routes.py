from . import auth
from .forms import LoginForm, SignUpForm
from flask import request, flash, render_template, redirect, url_for
from app.models import User
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user

@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST' and form.validate_on_submit():
        email = form.email.data
        password = form.password.data
        user = User.query.filter(User.email == email).first()
        print(user)
        if user and check_password_hash(user.password, password):
            login_user(user)
            flash('Succesfully Logged in!', 'success')
            return redirect(url_for('main.home'))
        else:
            flash('Invalid Email or Password', 'warning')
            return render_template('login.html', form=form)
    else:
        return render_template('login.html', form=form)
    
@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    form = SignUpForm()
    if request.method == 'POST' and form.validate_on_submit():
        username = form.username.data
        email = form.email.data
        password = form.password.data
        #build my user in my db
        user = User(username, email, password)
        user.save()

        flash('Thank you for signing up!', 'success')
        return redirect(url_for('auth.login'))
    else:
        return render_template('signup.html', form=form)
    
@auth.route('/logout')
def logout():
    flash('Successfully logged out', 'info')
    logout_user()
    return redirect(url_for('auth.login'))