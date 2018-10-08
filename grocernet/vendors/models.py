from grocernet.db import db
from grocernet.util.ratings import get_rating_average
from geoalchemy2.types import Geography
from geoalchemy2.shape import to_shape


class Vendor(db.Model):
    """
    Represents a business that sells produce.
    """
    def __init__(self, name, address, latitude_longitude):
        self.name = name
        self.address = address
        self.latitude_longitude = latitude_longitude

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    address = db.Column(db.String(200), nullable=False)
    latitude_longitude = db.Column(Geography("POINT"), nullable=False)
    
    avg_rating = db.Column(db.Float(), default=0.00)
    # relationship to rating
    ratings = db.relationship('Rating', backref="vendor", lazy=True)
    
    def update_average_rating(self):
        avg_rating = get_rating_average(self.ratings)

    def __repr__(self):
        return '<Vendor %r>' % self.name

    def to_dict(self):
        point = to_shape(self.latitude_longitude)
        latlon = [point.x, point.y]
        return {
            "id": self.id,
            'name': self.name,
            'address': self.address,
            'location': latlon
        }


class Rating(db.Model):
    def __init__(self, rating, vendor_id, user_id):
        self.rating = rating
        self.vendor_id = vendor_id
        self.user_id = user_id

    id = db.Column(db.Integer, primary_key=True)

    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(2000))
    purchase_list = db.Column(db.String(500))

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'),
                          nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
