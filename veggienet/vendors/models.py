from veggienet.db import db
from veggienet.util.geo import geocode_address
from geoalchemy2.types import Geography


class Vendor(db.Model):
    """
    Represents a business that sells produce.
    """

    def __init__(self, name, address):
        self.name = name

        data = geocode_address(address)
        self.address = data[0]
        self.latitude_longitude = "POINT(" + str(data[1][0]) + \
                                  " " + str(data[1][1]) + ")"

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    vendor_type = db.Column(db.String(10), default="store")
    address = db.Column(db.String(200), nullable=False)
    latitude_longitude = db.Column(Geography("POINT"), nullable=False)

    def __repr__(self):
        return '<Vendor %r>' % self.name
