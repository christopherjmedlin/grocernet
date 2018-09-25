from veggienet.db import db
from veggienet.util.geo import geocode_address, parse_postgis_point
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

    def __repr__(self):
        return '<Vendor %r>' % self.name

    def to_dict(self):
        point = to_shape(self.latitude_longitude)
        latlon = [point.x, point.y]
        return {
            'name': self.name,
            'vendor_type': self.vendor_type,
            'address': self.address,
            'location': latlon
        }
