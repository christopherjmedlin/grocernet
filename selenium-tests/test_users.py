from selenium.webdriver.common.by import By
import random
import string


def fill_out_signup_form(selenium, username="username12345",
                         email="email@gmail.com",
                         password="p@$$w0rd12345",
                         confirm="p@$$w0rd12345"):
    """
    Helper for filling out signup form
    """
    selenium.find_element(By.ID, 'username').send_keys(username)
    selenium.find_element(By.ID, 'email').send_keys(email)
    selenium.find_element(By.ID, 'password').send_keys(password)
    selenium.find_element(By.ID, 'confirm').send_keys(confirm)
    selenium.find_element(By.XPATH,
                          '//*[@id="signup-box"]/form/input[6]').click()


def fill_out_login_form(selenium, username, password):
    """
    Helper for filling out login form
    """
    user_xpath = '//*[@id="login-box"]/form/input[1]'
    pass_xpath = '//*[@id="login-box"]/form/input[2]'
    submit_xpath = '//*[@id="login-box"]/form/input[4]'
    selenium.find_element(By.XPATH, user_xpath).send_keys(username)
    selenium.find_element(By.XPATH, pass_xpath).send_keys(password)
    selenium.find_element(By.XPATH, submit_xpath).click()


def random_string(length):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


def test_invalid_login(selenium, test_server_url, test_user, test_password):
    selenium.get(test_server_url + "/login")

    # enter invalid username and password and submit
    fill_out_login_form(selenium, test_user, test_password+"bad")

    error = selenium.find_element(By.CLASS_NAME, "error")
    assert error
    assert selenium.current_url == test_server_url + "/login"
    assert "Invalid username or password" in error.text


def test_valid_login(selenium, test_server_url, test_user, test_password):
    fill_out_login_form(selenium, test_user, test_password)

    assert selenium.current_url == test_server_url + "/"
    account_dropdown_button = selenium.find_element(By.ID,
                                                    "account-dropdown-button")
    assert test_user in account_dropdown_button.text


def test_logout(selenium, test_server_url):
    selenium.get(test_server_url + "/logout")

    assert selenium.current_url == test_server_url + "/"
    login_signup = selenium.find_element(By.ID, "login-signup")
    assert "Log In" in login_signup.text
    assert "Sign Up" in login_signup.text


def test_invalid_signup(selenium, test_server_url, test_user, test_password):
    selenium.get(test_server_url + "/signup")

    # already existing username test
    fill_out_signup_form(selenium, username=test_user)
    err = selenium.find_element(By.XPATH, '//*[@id="signup-box"]/form/p')
    assert "Username already taken" in err.text

    # invalid password and email test
    fill_out_signup_form(selenium, email="notanemail:P", password="short")
    email_err = selenium.find_element(By.XPATH,
                                      '//*[@id="signup-box"]/form/p[1]')
    pass_err = selenium.find_element(By.XPATH,
                                     '//*[@id="signup-box"]/form/p[2]')

    assert "Invalid email address." in email_err.text
    assert "Password should be over 8 characters long" in pass_err.text

    # long username test
    username = ""
    for i in range(50):
        username += "$"
    fill_out_signup_form(selenium, username=username)
    err = selenium.find_element(By.XPATH, '//*[@id="signup-box"]/form/p')

    assert "must be less than 40 characters" in err.text


def test_valid_signup(selenium, test_server_url):
    selenium.get(test_server_url + "/signup")

    password = random_string(30)
    username = random_string(30)
    email = random_string(20) + "@" + random_string(5) + ".com"
    fill_out_signup_form(selenium, username=username,
                         email=email, password=password,
                         confirm=password)
    
    assert "/email/verification-sent" in selenium.current_url
    # split with @ symbol because of the email censoring
    assert email.split("@")[1] in selenium.find_element(By.ID, "content").text

    # ensure that an attempted login will result in the
    # email verification sent page
    selenium.get(test_server_url + "/login")
    fill_out_login_form(selenium, username, password)
    assert "/email/verification-sent" in selenium.current_url


def test_email_verification_invalid_token(selenium, test_server_url):
    selenium.get(test_server_url + "/email/verify/notatoken")
    response = selenium.find_element(By.ID, "content").text
    assert "Invalid email token" in response
