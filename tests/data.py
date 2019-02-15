from app.models import User, Place, Category, Booking, Facility, BookingFacility, MapPoint
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
        'category_id': 1
    },
    {
        'category_id': 1
    },
    {
        'category_id': 1
    },
    {
        'category_id': 1
    },
    {
        'category_id': 1
    },
    {
        'category_id': 1
    },
    {
        'category_id': 1
    },
]
bookings = [
    {
        'place_id': 1,
        'user_id': 1,
        'booking_date': date(2019, 2, 11),
        'internal_booking_status': 'Booked'
    },
    {
        'place_id': 2,
        'user_id': 1,
        'booking_date': date(2019, 2, 13),
        'internal_booking_status': 'Booked'
    },
]

points = [
    {
        'x_coordinate': 0,
        'y_coordinate': 0,
        'place_id': 1
    },
    {
        'x_coordinate': 1,
        'y_coordinate': 0
    },
    {
        'x_coordinate': 2,
        'y_coordinate': 0,
        'place_id': 2
    },
    {
        'x_coordinate': 3,
        'y_coordinate': 0
    },
    {
        'x_coordinate': 4,
        'y_coordinate': 0,
        'place_id': 3
    },
    {
        'x_coordinate': 0,
        'y_coordinate': 1
    },
    {
        'x_coordinate': 1,
        'y_coordinate': 1
    },
    {
        'x_coordinate': 2,
        'y_coordinate': 1
    },
    {
        'x_coordinate': 3,
        'y_coordinate': 1
    },
    {
        'x_coordinate': 4,
        'y_coordinate': 1
    },
    {
        'x_coordinate': 0,
        'y_coordinate': 2,
        'place_id': 4
    },
    {
        'x_coordinate': 1,
        'y_coordinate': 2
    },
    {
        'x_coordinate': 2,
        'y_coordinate': 2,
        'place_id': 5
    }

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

for point in points:
    c = MapPoint(**point)
    db.session.add(c)
    print('Added {}'.format(c))
    db.session.commit()
