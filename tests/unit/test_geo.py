import pytest

from veggienet.util import geo
import os


@pytest.mark.skipif("MAPBOX_ACCESS_TOKEN" not in os.environ,
                    reason="No mapbox token found.")
def test_geocode_address():
    test_address = "701 sw 6th ave portland"
    data = geo.geocode_address(test_address)

    assert data[1][0] == -122.67928
    assert data[1][1] == 45.518886
    assert data[0] == "701 Southwest 6th Avenue, Portland, " \
                      "Oregon 97204, United States"


def test_geocode_invalid_address():
    data = geo.geocode_address("fsadjkl;asdfkl;jadsf")
    assert data is None


def test_parse_postgis_point():
    point_string = "POINT(2.31324 5.3432)"
    assert geo.parse_postgis_point(point_string) == [2.31324, 5.3432]
    point_string = "POINT(2 5)"
    assert geo.parse_postgis_point(point_string) == [2.0, 5.0]

    with pytest.raises(ValueError) as err:
        geo.parse_postgis_point("not a valid point")
    assert "Invalid PostGIS point." in str(err.value)
