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

def finish_first_order():
    driver, actions = initialize_browser()

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

    finally:
        driver.quit()


if __name__ == "__main__":
    finish_first_order()