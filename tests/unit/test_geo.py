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
    assert data[0] == "701 Southwest 6th Avenue, Portland," \
                      "Oregon 97204, United States"
