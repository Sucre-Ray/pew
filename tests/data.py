from app.models import User, Place, Category, Booking, Facility, BookingFacility
from app import db
from datetime import date

categories = [
    {
        'category_name': 'simple',
        'description': 'simple places',
        'price': 100
    }
]

places = [
    {
        'top_coordinate': 0,
        'down_coordinate': 1,
        'left_coordinate': 0,
        'right_coordinate': 1,
        'floor': 1,
        'category_id': 1
    },
    {
        'top_coordinate': 0,
        'down_coordinate': 1,
        'left_coordinate': 2,
        'right_coordinate': 3,
        'floor': 1,
        'category_id': 1
    },
    {
        'top_coordinate': 0,
        'down_coordinate': 1,
        'left_coordinate': 4,
        'right_coordinate': 5,
        'floor': 1,
        'category_id': 1
    },
]
bookings = [
    {
        'place_id': 1,
        'user_id': 1,
        'booking_start': date(2019, 2, 11),
        'booking_end': date(2019, 2, 11),
        'internal_booking_status': 'Booked'
    },
    {
        'place_id': 2,
        'user_id': 1,
        'booking_start': date(2019, 2, 13),
        'booking_end': date(2019, 2, 14),
        'internal_booking_status': 'Booked'
    },
]
for category in categories:
    c = Category(**category)
    db.session.add(c)
    print('Added {}'.format(c))
    db.session.commit()
for place in places:
    c = Place(**place)
    db.session.add(c)
    print('Added {}'.format(c))
    db.session.commit()
for booking in bookings:
    c = Booking(**booking)
    db.session.add(c)
    print('Added {}'.format(c))
    db.session.commit()


