import pytest
import os
from veggienet.users.models import User
from veggienet.vendors.models import Vendor


def test_user():
    username = "user12345"
    password = "s3cur3p@$$word"
    email = "email@gmail.com"
    user = User(username, password, email, False)

    assert user.password != password
    assert "pbkdf2:sha256" in user.password
    assert user.username is username
    assert user.email is email
    assert not user.admin

    user.set_password("newpassword")
    assert user.password != "newpassword"

    dictionary = user.to_dict()
    assert dictionary["username"] == username
    assert "password" not in dictionary
    assert not dictionary["admin"]

    assert str(user) == "<User 'user12345'>"


@pytest.mark.skipif("MAPBOX_ACCESS_TOKEN" not in os.environ,
                    reason="No mapbox token found.")
def test_vendor():
    vendor = Vendor("Safeway", "1010 sw jefferson street portland")

    expected_address = "1010 Southwest Jefferson Street, " \
                       "Portland, Oregon 97201, United States"
    assert vendor.name == "Safeway"
    assert vendor.address == expected_address
    assert vendor.latitude_longitude == "POINT(-122.68496 45.515816)"

    assert str(vendor) == "<Vendor 'Safeway'>"
