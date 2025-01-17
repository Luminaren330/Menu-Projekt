import time
from selenium.webdriver.common.by import By

class base_actions:
    def __init__(self, driver):
        self.driver = driver

    def login(self, email: str, password: str) -> None:
        self.driver.get("http://localhost:3000/login")

        login_input = self.driver.find_element(By.ID, "username")
        login_input.send_keys(email)

        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(password)

        login_button = self.driver.find_element(By.CLASS_NAME, "Login_button__sOnZe")
        login_button.click()

        time.sleep(1)
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(2)

        logout_button = self.driver.find_element(By.CLASS_NAME, "Navbar_logout_button__DjflN")
        assert logout_button is not None, "Logowanie nie powiodło się!"

    def register(self, username: str, password: str, firstname: str, lastname: str, phoneNumber: str) -> None:
        self.driver.get("http://localhost:3000/login")

        login_input = self.driver.find_element(By.CLASS_NAME, "Login_link__7KtW-")
        login_input.click()

        login_input = self.driver.find_element(By.ID, "username")
        login_input.send_keys(username)

        password_input = self.driver.find_element(By.ID, "password")
        password_input.send_keys(password)

        password_input = self.driver.find_element(By.ID, "firstName")
        password_input.send_keys(firstname)

        password_input = self.driver.find_element(By.ID, "lastName")
        password_input.send_keys(lastname)

        password_input = self.driver.find_element(By.ID, "phoneNumber")
        password_input.send_keys(phoneNumber)

        login_button = self.driver.find_element(By.CLASS_NAME, "Login_button__sOnZe")
        login_button.click()

        time.sleep(1)
        alert = self.driver.switch_to.alert
        alert.accept()
        time.sleep(2)

        logout_button = self.driver.find_element(By.CLASS_NAME, "Navbar_logout_button__DjflN")
        assert logout_button is not None, "Rejestracja nie powiodła się!"
