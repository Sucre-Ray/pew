from werkzeug.urls import url_parse

from app import app, db
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, LoginForm, ResetPasswordForm, ResetPasswordRequestForm
from app.models import User
from app.mail import send_password_reset_email, send_email_activate_email


@login_required
@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data,
                                    status='Active').first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid email or password, '
                  'or user haven\'t been activated.')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Login', form=form)


@app.route('/activate_user/<token>')
def activate_user(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(username=form.username.data,
                    email=form.email.data,
                    status='Registered')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_email_activate_email(user)
        return redirect(url_for('email_confirm'))
    return render_template('register.html', title='Register', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/user/<id>')
@login_required
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    return render_template('user.html', user=user)


@app.route('/reset_password_confirm')
def reset_password_confirm():
    return render_template('reset_password_confirm.html')

@app.route('/register_email_confirm')
def register_email_confirm():
    return render_template('register_email_confirm.html')

@app.route('/email_confirm/<token>')
def email_confirm(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_user_id_token(token)
    if not user:
        return redirect(url_for('index'))
    if not user.is_active():
        user.activate()
        db.session.commit()
    # As a possibility to do login user from token
    # login_user(user)
    return redirect(url_for('login'))


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('reset_password_confirm'))
    return render_template('reset_password_request.html',
                           title='Reset Password',
                           form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_user_id_token(token)
    if not user:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('login'))
    return render_template('reset_password.html', form=form)

