import pytest
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

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


@pytest.fixture(scope="session")
def test_server_url(request):
    return request.config.getoption("--testprotocol") + "://" + \
           request.config.getoption("--testhost") + ":" + \
           request.config.getoption("--testport")

@pytest.fixture(scope="session")
def test_user(request):
    return request.config.getoption("--testuser")

@pytest.fixture(scope="session")
def test_password(request):
    return request.config.getoption("--testpassword")

@pytest.fixture(scope='session')
def selenium(test_server_url):
    chrome_options = Options()
    chrome_options.add_argument("start-fullscreen")
    
    selenium = webdriver.Chrome(chrome_options=chrome_options)
    selenium.get(test_server_url)
    yield selenium
    selenium.quit()
