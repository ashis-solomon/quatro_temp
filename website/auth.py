from flask import Blueprint, render_template, request, flash, redirect, url_for
from .models import User
from werkzeug.security import generate_password_hash, check_password_hash
from . import db
from flask_login import login_user, login_required, logout_user, current_user


auth = Blueprint('auth', __name__)


@auth.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash('Logged in successfully!', category='success')
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash('Incorrect password, try again.', category='error')
        else:
            flash('Email does not exist.', category='error')

    return render_template("login.html", user=current_user)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('auth.login'))


@auth.route('/sign-up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        empty_str = None
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=first_name, org_bool=0, org_name=empty_str, org_volunteers=empty_str, org_lat=empty_str, org_long=empty_str
            ,password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)

# -----------------------------------------------------------------------------------------------------------------

@auth.route('/org-login', methods=['GET', 'POST'])
def org_login():
    # if request.method == 'POST':
    #     email = request.form.get('email')
    #     password = request.form.get('password')

    #     user = User.query.filter_by(email=email).first()
    #     if user:
    #         if check_password_hash(user.password, password):
    #             flash('Logged in successfully!', category='success')
    #             login_user(user, remember=True)
    #             return redirect(url_for('views.home'))
    #         else:
    #             flash('Incorrect password, try again.', category='error')
    #     else:
    #         flash('Email does not exist.', category='error')

    return render_template("login_org.html", user=current_user)


# @auth.route('/logout')
# @login_required
# def logout():
#     logout_user()
#     return redirect(url_for('auth.login'))


@auth.route('/org-sign-up', methods=['GET', 'POST'])
def org_sign_up():
    if request.method == 'POST':
        email = request.form.get('email')
        orgName = request.form.get('orgName')
        orgTypes = request.form.get('orgTypes')
        orgVol = request.form.get('orgVol')
        orgLat = request.form.get('orgLat')
        orgLong = request.form.get('orgLong')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        empty_str = None
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists.', category='error')
        elif len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(orgName) < 2:
            flash('Organization name must be greater than 1 character.', category='error')
        elif password1 != password2:
            flash('Passwords don\'t match.', category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            new_user = User(email=email, first_name=empty_str, org_bool=1, org_name=orgName, org_types=orgTypes, org_volunteers=orgVol, org_lat=orgLat, org_long=orgLong
            ,password=generate_password_hash(
                password1, method='sha256'))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash('Account created!', category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up_org.html", user=current_user)

