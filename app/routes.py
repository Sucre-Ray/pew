from werkzeug.urls import url_parse

from app import app, db
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_user, logout_user, login_required, current_user
from app.forms import RegisterForm, LoginForm, ResetPasswordForm, \
    ResetPasswordRequestForm, EditProfileForm, ChangePasswordForm, BookingDateForm
from app.models import User, MapPoint, Place, Booking
from sqlalchemy import distinct
from app.mail import send_password_reset_email, send_email_activate_email
from datetime import date, datetime


@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<book_date>', methods=['GET', 'POST'])
@login_required
def index(book_date=None):
    form = BookingDateForm()
    rows = [row[0] for row in db.session.query(distinct(MapPoint.y_coordinate)).all()]
    points = {row: MapPoint.query.filter_by(y_coordinate=row).all() for row in rows}
    if request.method == 'GET' and book_date:
        form.date.data = book_date
    if request.method == 'GET' and not book_date:
        form.date.data = date.today()
    if form.validate_on_submit():
        return redirect(url_for('index', book_date=form.date.data))
    return render_template('index.html', points=points, form=form)



@app.route('/book/<place>/<book_date>')
@login_required
def book(book_date, place):
    place = Place.query.filter_by(id=place).first_or_404()
    if place.is_booked_on_date(book_date):
        flash('This place is booked on chosen date. Please choose another one.')
        return redirect(url_for('index', book_date=book_date))
    booking = Booking(place_id=place.id,
                      user_id=current_user.id,
                      booking_date=datetime.strptime(book_date, '%Y-%m-%d').date())
    db.session.add(booking)
    db.session.commit()
    return render_template('book.html', booking=booking)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None \
                or (not user.check_password(form.password.data)) \
                or (not user.is_active()):
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
        user = User(name=form.name.data,
                    email=form.email.data,
                    status='Registered')
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        send_email_activate_email(user)
        return redirect(url_for('register_email_confirm'))
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
        flash('Your account successfully activated.')
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



@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    profile_form = EditProfileForm()
    password_form = ChangePasswordForm()
    if profile_form.validate_on_submit():
        current_user.name = profile_form.name.data
        current_user.bio = profile_form.bio.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        profile_form.name.data = current_user.name
        profile_form.bio.data = current_user.bio
    elif password_form.validate_on_submit():
        # user = User.query.filter_by(email=current_user.email).first()
        if not current_user.check_password(password_form.old_password.data):
            flash('Old password is incorrect.')
            return redirect(url_for('edit_profile'))
        current_user.set_password(password_form.new_password.data)
        db.session.commit()
        flash('Your password successfully changed.')
        return redirect(url_for('edit_profile'))
    return render_template('edit_profile.html',
                           title='Edit Profile',
                           profile_form=profile_form,
                           password_form=password_form,
                           user=current_user)

@app.route('/cancel_booking', methods=['POST'])
@login_required
def cancel_booking():
    return jsonify({'text': Booking.cancel(request.form['id']),
                    'booking_status': Booking.query.get(int(request.form['id'])).get_status()})
