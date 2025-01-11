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
