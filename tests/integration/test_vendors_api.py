import pytest
from veggienet.vendors.models import Vendor
from veggienet.db import save_to_database
from veggienet.util.geo import parse_postgis_point
from geoalchemy2.shape import to_shape


def query_vendor(vendor_id):
    return Vendor.query.filter_by(id=vendor_id).first()


@pytest.fixture(scope="module")
def vendor(app):
    vendor = Vendor("Safeway", "1010 sw jefferson street portland")
    save_to_database(vendor)
    return query_vendor(vendor.id) 

def test_vendor_retrieve(vendor, client):
    response = client.get('/api/v1/vendors/' + str(vendor.id))
    data = response.data.decode('utf-8')

    assert vendor.name in data
    assert vendor.address in data
    latlon = to_shape(vendor.latitude_longitude)
    assert str(latlon.x) in data
    assert str(latlon.y) in data
