from operator import le
from flask import Blueprint, render_template, redirect, request, flash
from flask.helpers import url_for
from models import User
from flask_login import login_user, login_required, logout_user, current_user

auth = Blueprint('auth', __name__)

@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if user.verify_password(password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exits.', category='error')
    return render_template("signin/index.html", boolean= True)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        email = request.form.get('email')
        username = request.form.get('username')
        password = request.form.get('password')
        repassword = request.form.get('repassword')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(username) < 2:
            flash('Username must be greater than 1 character.', category='error')
        elif password != repassword:
            flash('Password don\'t match.', category= 'error')
        elif len(password) < 6:
            flash('Password must be at least 7 characters.', category= 'error')
        else:
            new_user = User(email=email, username=username, password = password)
            from initial import db
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user , remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("signup/index.html")