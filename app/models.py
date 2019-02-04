from app import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login
from hashlib import md5


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    name = db.Column(db.String(100))
    surname = db.Column(db.String(100))
    birth_date = db.Column(db.Date)
    bio = db.Column(db.String(300))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    bookings = db.relationship('Booking',
                               backref=db.backref('creator', lazy=True))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(
            digest, size)


class Place(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    top_coordinate = db.Column(db.Integer)
    down_coordinate = db.Column(db.Integer)
    left_coordinate = db.Column(db.Integer)
    right_coordinate = db.Column(db.Integer)
    floor = db.Column(db.Integer)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'))

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
        return '<Category {}>'.format(self.categoryname)


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
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Booking id:{};place:{};user:{}>'.format(self.id,
                                                         self.place_id,
                                                         self.user_id)


class BookingFacility(db.Model):
    booking_id = db.Column(db.Integer, db.ForeignKey('booking.id'), primary_key=True)
    facility_id = db.Column(db.Integer, db.ForeignKey('facility.id'), primary_key=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    updated = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Facility {}>'.format(self.name)
