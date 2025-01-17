from selenium import webdriver
from selenium.webdriver.common.by import By
import base_actions
import time

def initialize_browser():
    options = webdriver.ChromeOptions()
    options.add_argument("--start-maximized")
    options.add_argument("--disable-notifications")
    driver = webdriver.Chrome(options=options)
    actions = base_actions.base_actions(driver)
    return driver, actions

def register_new_user():
    try:
        actions.register("new_username", "123", "Imie", "Nazwisko", "123123123")

        yourorder_link = driver.find_element(By.XPATH, "//a[@href='/yourorder']")
        yourorder_link.click()
        time.sleep(1)

        yourorder_value = driver.find_element(By.XPATH, "//div[@class='OrderItems_menuItems__GeTL7']//h2[normalize-space()='Suma: 0 zł']")
        assert yourorder_value is not None, "Niepoprawny stan menu dla nowego konta"

        orders_link = driver.find_element(By.XPATH, "//a[@href='/orders']")
        orders_link.click()
        time.sleep(1)

        table = driver.find_element(By.CLASS_NAME, "Orders_orderTable__PQzeO")
        rows = table.find_elements(By.XPATH, ".//thead/tr")
        assert rows != 1, "Niezgodna ilość kolumn w zamówieniach"

    except Exception as e:
        print(f"Wystąpił błąd podczas testu stanu nowego konta: {e}")

def finish_first_order():
    try:
        actions.login("student", "123")

        menu_link = driver.find_element(By.LINK_TEXT, "Zamówienia")
        menu_link.click()

        time.sleep(1)
        finish_order = driver.find_element(By.CLASS_NAME, "Orders_deleteButton__xEcL3")
        finish_order.click()
        time.sleep(1)

    except Exception as e:
        print(f"Wystąpił błąd podczas testu usuwania z menu: {e}")

def made_order():
    try:
        actions.login("Jacek", "123")

        menu_link = driver.find_element(By.XPATH, "//a[@href='/menu']")
        menu_link.click()
        time.sleep(1)

        quantity = driver.find_element(By.XPATH, "//path[@d='M416 208H272V64c0-17.67-14.33-32-32-32h-32c-17.67 0-32 14.33-32 32v144H32c-17.67 0-32 14.33-32 32v32c0 17.67 14.33 32 32 32h144v144c0 17.67 14.33 32 32 32h32c17.67 0 32-14.33 32-32V304h144c17.67 0 32-14.33 32-32v-32c0-17.67-14.33-32-32-32z']")
        quantity.click()
        time.sleep(1)

        add_to_order = driver.find_element(By.CLASS_NAME, "Menu_orderButton__DDSQy")
        add_to_order.click()
        time.sleep(1)

        yourorder_link = driver.find_element(By.CLASS_NAME, "Menu_yourOrderBtn__j9kGZ")
        yourorder_link.click()
        time.sleep(1)

        delete_button = driver.find_element(By.CLASS_NAME, "OrderItems_deleteBtn__BKZ3y")
        assert delete_button is not None, "Nie dania do zamówienia zamówienia"
        time.sleep(1)

        choose_place_link = driver.find_element(By.XPATH, "//a[@href=\"/chooseplace\"]")
        choose_place_link.click()
        time.sleep(1)

        choose_place = driver.find_element(By.CLASS_NAME, "ChoosePlace_card__yGfbs")
        choose_place.click()
        time.sleep(1)

        date = driver.find_element(By.CLASS_NAME, "rdtSwitch")
        date.send_keys("value", "January 2026")
        time.sleep(1)

    except Exception as e:
        print(f"Wystąpił błąd podczas testu usuwania z menu: {e}")

if __name__ == "__main__":
    driver, actions = initialize_browser()
    # finish_first_order()
    made_order()
    # register_new_user()
    driver.quit()
