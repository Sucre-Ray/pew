from app import app, db, login
from datetime import datetime, date
from time import time
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from hashlib import md5
import jwt


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    bio = db.Column(db.String(300))
    status = db.Column(db.String(20))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bookings = db.relationship('Booking',
                               backref=db.backref('creator', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def activate(self):
        self.status = 'Active'

    def deactivate(self):
        self.status = 'Deactivated'

    def is_active(self):
        return self.status == 'Active'

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)

    def get_user_id_token(self, expires_in=600):
        return jwt.encode(
            {'user_id': self.id, 'exp': time() + expires_in},
            app.config['SECRET_KEY'], algorithm='HS256').decode('utf-8')

    @staticmethod
    def verify_user_id_token(token):
        try:
            id = jwt.decode(token, app.config['SECRET_KEY'],
                            algorithms=['HS256'])['user_id']
        except:
            return
        return User.query.get(id)

    def get_user_bookings(self):
        return Booking.query.filter_by(user_id=self.id).\
            order_by(Booking.booking_start.desc()).all()


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    top_coordinate = db.Column(db.Integer)
    down_coordinate = db.Column(db.Integer)
    left_coordinate = db.Column(db.Integer)
    right_coordinate = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))
    bookings = db.relationship('Booking', backref=db.backref('place', lazy=True))

    def __repr__(self):
        return '<Place {}>'.format(self.id)


class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    category_name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(500))
    price = db.Column(db.Integer)
    category_places = db.relationship('Place',
                                      backref=db.backref('category', lazy=True))

    def __repr__(self):
        return '<Category {}>'.format(self.category_name)


class Facility(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True)
    description = db.Column(db.String(1000))
    price = db.Column(db.Integer)

    def __repr__(self):
        return '<Facility {}>'.format(self.name)


class Booking(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    place_id = db.Column(db.Integer, db.ForeignKey('place.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    booking_start = db.Column(db.Date)
    booking_end = db.Column(db.Date)
    internal_booking_status = db.Column(db.String(100), default='Booked', index=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime)
    facilities = db.relationship('BookingFacility',
                                 backref=db.backref('booking', lazy=True))

    def __repr__(self):
        return '<Booking id:{};place:{};user:{}>'.format(self.id,
                                                         self.place_id,
                                                         self.user_id)

    def get_status(self):
        if self.booking_end < date.today() and self.internal_booking_status == 'Booked':
            return 'Closed'
        elif self.booking_end >= date.today() >= self.booking_start \
                and self.internal_booking_status == 'Booked':
            return 'In progress'
        elif self.booking_start > date.today():
            return 'New'
        elif self.internal_booking_status == 'Cancelled':
            return self.internal_booking_status

    def get_place_price(self):
        return Booking.query.filter_by(id=self.id).first().place.category.price


class BookingFacility(db.Model):
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime)

    def __repr__(self):
        return '<Facility {}>'.format(self.name)
