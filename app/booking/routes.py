from app import db
from app.booking import bp
from flask import render_template, flash, redirect, url_for, request, jsonify
from flask_login import login_required, current_user
from app.booking.forms import BookingDateForm
from app.models import MapPoint, Place, Booking
from sqlalchemy import distinct
from datetime import date, datetime


@bp.route('/index', methods=['GET', 'POST'])
@bp.route('/index/<book_date>', methods=['GET', 'POST'])
def index(book_date=None):
    form = BookingDateForm()
    rows = [row[0] for row in db.session.query(distinct(MapPoint.y_coordinate)).all()]
    points = {row: MapPoint.query.filter_by(y_coordinate=row).all() for row in rows}
    if request.method == 'GET' and book_date:
        form.date.data = book_date
    if request.method == 'GET' and not book_date:
        form.date.data = date.today()
    if form.validate_on_submit():
        return redirect(url_for('booking.index', book_date=form.date.data))
    return render_template('booking/index.html', points=points, form=form)


@bp.route('/book/<place>/<book_date>')
@login_required
def book(book_date, place):
    place = Place.query.filter_by(id=place).first_or_404()
    if place.is_booked_on_date(book_date):
        flash('This place is booked on chosen date. Please choose another one.')
        return redirect(url_for('booking.index', book_date=book_date))
    booking = Booking(place_id=place.id,
                      user_id=current_user.id,
                      booking_date=datetime.strptime(book_date, '%Y-%m-%d').date())
    db.session.add(booking)
    db.session.commit()
    return render_template('booking/book.html', booking=booking)


@bp.route('/cancel_booking', methods=['POST'])
@login_required
def cancel_booking():
    return jsonify({'text': Booking.cancel(request.form['id']),
                    'booking_status': Booking.query.get(int(request.form['id'])).get_status()})
