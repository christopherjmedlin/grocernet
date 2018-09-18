import pytest

from veggienet.util import geo
import os


@pytest.mark.skipif("MAPBOX_ACCESS_TOKEN" not in os.environ,
                    reason="No mapbox token found.")
def test_geocode_address():
    test_address = "701 SW 6th Ave, Portland, OR 97205"
    coords = geo.geocode_address(test_address)
    
    assert coords[0] == -122.67928
    assert coords[1] == 45.518886
