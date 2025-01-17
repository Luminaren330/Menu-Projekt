from selenium import webdriver
import requests

driver = webdriver.Chrome()

api_url = "http://127.0.0.1:5000/register"
headers = {
    "Content-Type": "application/json",
}
payload = {
    "email": "student",
    "password": "123",
    "role": "admin"
}

response = requests.post(api_url, json=payload, headers=headers)

if response.status_code == 200:
    print("Rejestracja przez API powiodła się:", response.json())
else:
    print(f"Błąd rejestracji API: {response.status_code} {response.text}")

# Zakończenie pracy Selenium
driver.quit()
