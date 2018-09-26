from veggienet.db import db
from geoalchemy2.types import Geography
from geoalchemy2.shape import to_shape


class Vendor(db.Model):
    """
    Represents a business that sells produce.
    """
    def __init__(self, name, address, vendor_type, latitude_longitude):
        self.name = name
        self.address = address
        self.vendor_type = vendor_type
        self.latitude_longitude = latitude_longitude

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    vendor_type = db.Column(db.String(10), default="store")
    address = db.Column(db.String(200), nullable=False)
    latitude_longitude = db.Column(Geography("POINT"), nullable=False)

    # relationship to rating
    ratings = db.relationship('Rating', backref="vendor", lazy=True)

    def __repr__(self):
        return '<Vendor %r>' % self.name

    def to_dict(self):
        point = to_shape(self.latitude_longitude)
        latlon = [point.x, point.y]
        return {
            "id": self.id,
            'name': self.name,
            'vendor_type': self.vendor_type,
            'address': self.address,
            'location': latlon
        }


class Rating(db.Model):
    def __init__(self, rating, vendor_id, user_id):
        if self.rating <= 5 and self.rating >= 1:
            self.rating = rating
        else:
            raise ValueError("Rating must be between 1 and 5")

    id = db.Column(db.Integer, primary_key=True)

    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.String(2000))
    purchase_list = db.Column(db.String(500))

    vendor_id = db.Column(db.Integer, db.ForeignKey('vendor.id'),
                          nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),
                        nullable=False)
