import pytest

def pytest_addoption(parser):
    parser.addoption(
        "--testhost", action="store", default="localhost", help="Host of test server."
    )
    parser.addoption(
        "--testport", action="store", default="5000", help="Port of test server."
    )
    parser.addoption(
        "--testprotocol", action="store", default="http", help="Protocol of test server (http or https)."
    )
    parser.addoption(
        "--testuser", action="store", default="username", help="Test username."
    )
    parser.addoption(
        "--testpassword", action="store", default="username", help="Test password."
    )


@pytest.fixture
def test_server_url(request):
    return request.config.getoption("--testprotocol") + "://" + \
           request.config.getoption("--testhost") + ":" + \
           request.config.getoption("--testport")

@pytest.fixture
def test_user(request):
    return request.config.getoption("--testuser")

@pytest.fixture
def test_password(request):
    return request.config.getoption("--testpassword")

@pytest.fixture
def selenium(selenium, test_server_url):
    # always start on homepage
    selenium.get(test_server_url)
    return selenium
