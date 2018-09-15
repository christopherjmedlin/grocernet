import pytest
from selenium.webdriver.common.by import By
import time

def test_invalid_login(selenium, test_server_url, test_user, test_password):
    # click login link
    selenium.find_element(By.XPATH, '//*[@id="login-signup"]/a[1]').click()

    # enter invalid username and password and submit
    selenium.find_element(By.XPATH, '//*[@id="login-box"]/form/input[1]').send_keys(test_user)
    selenium.find_element(By.XPATH, '//*[@id="login-box"]/form/input[2]').send_keys(test_password+"bad")
    selenium.find_element(By.XPATH, '//*[@id="login-box"]/form/input[4]').click()

    error = selenium.find_element(By.CLASS_NAME, "error")
    assert error
    assert selenium.current_url == test_server_url + "/login"
    assert "Invalid username or password" in error.text

def test_valid_login(selenium, test_server_url, test_user, test_password):
    selenium.find_element(By.XPATH, '//*[@id="login-signup"]/a[1]').click()
    selenium.find_element(By.XPATH, '//*[@id="login-box"]/form/input[1]').send_keys(test_user)
    selenium.find_element(By.XPATH, '//*[@id="login-box"]/form/input[2]').send_keys(test_password)
    selenium.find_element(By.XPATH, '//*[@id="login-box"]/form/input[4]').click()
    
    assert selenium.current_url == test_server_url + "/"
    account_dropdown_button = selenium.find_element(By.ID, "account-dropdown-button")
    assert test_user in account_dropdown_button.text

