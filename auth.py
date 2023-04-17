from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from models import User
from app import db

auth = Blueprint('auth', __name__)


@auth.route('/sign_in', methods=['GET', 'POST'])
def sign_in():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                # flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exists.', category='error')

    return render_template("auth/sign_in.html", user=current_user)


@auth.route('/sign_out')
@login_required
def sign_out():
    logout_user()
    return redirect(url_for('auth.sign_in'))


@auth.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        user = User.query.filter_by(email=email).first()

        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 1:
            flash('Email must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don`t much.', category='error')
        elif len(password1) < 7:
            flash('Passwords must be at least 7 characters.', category='error')
        else:
            # add user to db
            new_user = User(email=email,
                            first_name=first_name,
                            password=generate_password_hash(password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("auth/sign_up.html", user=current_user)
