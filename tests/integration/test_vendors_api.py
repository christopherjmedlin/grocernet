import pytest
import json
from veggienet.vendors.models import Vendor
from veggienet.db import save_to_database, db
from geoalchemy2.shape import to_shape


def query_vendor(vendor_id):
    return Vendor.query.filter_by(id=vendor_id).first()


def populate_database():
    db.session.add(
        Vendor("Albertson's", "5415 sw beaverton ave, portland",
               "store", "POINT(-122.732444 45.487854)")
    )
    db.session.add(
        Vendor("Portland Farmer's Market", "1799 sw park ave, portland",
               "market", "POINT(-122.732251 45.487822)")
    )
    # outside of portland
    db.session.add(
        Vendor("Safeway", "2201 E Madison St, Seattle, WA 98112",
               "store", "POINT(-122.313122 47.620334)")
    )
    db.session.commit()


@pytest.fixture(scope="module")
def vendor(app):
    vendor = Vendor("Safeway", "1010 sw jefferson street portland",
                    "store", "POINT(-122.684726 45.515668)")
    save_to_database(vendor)
    return query_vendor(vendor.id)


def test_vendor_retrieve(vendor, client):
    response = client.get('/api/v1/vendors/' + str(vendor.id))
    data = response.data.decode('utf-8')

    assert str(vendor.id) in data
    assert vendor.name in data
    assert vendor.address in data
    latlon = to_shape(vendor.latitude_longitude)
    assert str(latlon.x) in data
    assert str(latlon.y) in data


def test_vendor_list(vendor, client):
    populate_database()
    response = client.get('/api/v1/vendors/')
    data = json.loads(response.data.decode('utf-8'))

    assert len(data["vendors"]) is 4
    assert vendor.to_dict() in data["vendors"]


def test_vendor_list_points_only(vendor, client):
    query = {"points_only": True}
    response = client.get('/api/v1/vendors/', query_string=query)
    data = json.loads(response.data.decode('utf-8'))

    latlon = to_shape(vendor.latitude_longitude)
    assert [latlon.x, latlon.y] in data["vendors"]
    assert vendor.to_dict() not in data["vendors"]
    assert len(data["vendors"]) is 4


@pytest.mark.parametrize("start,end,expected_length", [
    (1, 2, 1), (1, 5, 3), (105, 200, 0)
])
def test_vendor_list_start_end(vendor, client,
                               start, end, expected_length):
    query = {"start": start,
             "end": end}
    response = client.get("/api/v1/vendors/", query_string=query)
    data = json.loads(response.data.decode('utf-8'))

    assert len(data["vendors"]) is expected_length


@pytest.mark.parametrize("point,expected_first", [
    ([47.2407301, -122.4403617], "Safeway"),
    ([-45.4884216, -122.7314334], "Portland Farmer's Market")
])
def test_vendor_list_distance_sort(vendor, client,
                                   point, expected_first):
    query = {"near_x": point[0], "near_y": point[1]}
    response = client.get("/api/v1/vendors/", query_string=query)
    data = json.loads(response.data.decode('utf-8'))

    assert len(data["vendors"]) is 4
    assert data["vendors"][0]["name"] == expected_first
