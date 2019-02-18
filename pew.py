from app import create_app, db
from app.models import User, Place, Booking, Facility, BookingFacility, Category, MapPoint

app = create_app()


@app.shell_context_processor
def make_shell_context():
    return {'db': db,
            'Place': Place,
            'User': User,
            'Booking': Booking,
            'Facility': Facility,
            'BookingFacility': BookingFacility,
            'Category': Category,
            'MapPoint': MapPoint}
