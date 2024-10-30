from browser import Browser
from config import AUTH_PASSWORD, AUTH_USER

browser = Browser()

browser.create_driver()
browser.navigate()
browser.auth(AUTH_USER, AUTH_PASSWORD)
while True:
    pass