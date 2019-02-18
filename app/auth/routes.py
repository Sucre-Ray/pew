from werkzeug.urls import url_parse
from app import db
from app.auth import bp
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, logout_user, current_user
from app.auth.forms import RegisterForm, LoginForm, ResetPasswordForm, \
    ResetPasswordRequestForm
from app.models import User
from app.auth.email import send_password_reset_email, send_email_activate_email


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('booking.index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None \
                or (not user.check_password(form.password.data)) \
                or (not user.is_active()):
            flash('Invalid email or password, '
                  'or user haven\'t been activated.')
            return redirect(url_for('auth.login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('booking.index')
        return redirect(next_page)
    return render_template('auth/login.html', title='Login', form=form)


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('booking.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        user = User(name=form.name.data,
                    email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_email_activate_email(user)
        return redirect(url_for('auth.register_email_confirm'))
    return render_template('auth/register.html', title='Register', form=form)


@bp.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('booking.index'))


@bp.route('/reset_password_confirm')
def reset_password_confirm():
    return render_template('auth/reset_password_confirm.html')


@bp.route('/register_email_confirm')
def register_email_confirm():
    return render_template('auth/register_email_confirm.html')


# TODO: change method to POST
@bp.route('/email_confirm/<token>')
def email_confirm(token):
    if current_user.is_authenticated:
        return redirect(url_for('booking.index'))
    user = User.verify_user_id_token(token)
    if not user:
        return redirect(url_for('booking.index'))
    if not user.is_active():
        user.activate()
        db.session.commit()
        flash('Your account successfully activated.')
    # As a possibility to do login user from token
    # login_user(user)
    return redirect(url_for('auth.login'))


@bp.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('booking.index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        return redirect(url_for('auth.reset_password_confirm'))
    return render_template('auth/reset_password_request.html',
                           title='Reset Password',
                           form=form)


@bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('booking.index'))
    user = User.verify_user_id_token(token)
    if not user:
        return redirect(url_for('booking.index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash('Your password has been reset.')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)
