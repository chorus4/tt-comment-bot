import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName, OperatingSystem
import json

class Browser:
    def __init__(self):
        pass

    def create_driver(self):
        uar = UserAgent(software_names=[SoftwareName.CHROME.value], operating_systems=[OperatingSystem.WINDOWS.value])

        options = webdriver.ChromeOptions()
        # Disable automation flags
        # options.add_argument("--disable-blink-features=AutomationControlled")
        # options.add_experimental_option("excludeSwitches", ["enable-automation"])
        # options.add_experimental_option("useAutomationExtension", False)
        # options.add_argument(f"user-agent={uar.get_random_user_agent()}")


        self.driver = webdriver.Chrome(options=options)

    def navigate(self, link = 'https://tiktok.com'):
        self.driver.get(link)

    def auth(self, auth_user, auth_users):
        try:
            with open('auth.json', 'r') as f:
                cookies = json.loads(f.read())
                if cookies[auth_user]:
                    for cookie in cookies[auth_user]:
                        self.driver.add_cookie(cookie)
                    self.driver.refresh()
                    return
        except Exception:
            pass

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.ID, "header-login-button"))
        ).click()

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[3]/div/div/div[1]/div[1]/div/div/div/div[2]/div[2]"))
        ).click()

        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[6]/div[3]/div/div/div[1]/div[1]/div/form/div[1]/a"))
        ).click()

        self.driver.find_element('xpath', '/html/body/div[6]/div[3]/div/div/div[1]/div[1]/div[2]/form/div[1]/input').send_keys(auth_user)
        self.driver.find_element('xpath', '/html/body/div[6]/div[3]/div/div/div[1]/div[1]/div[2]/form/div[2]/div/input').send_keys(auth_users)
        self.driver.find_element('xpath', '/html/body/div[6]/div[3]/div/div/div[1]/div[1]/div[2]/form/button').click()
        # time.sleep(10)

        WebDriverWait(self.driver, 50).until(
            EC.presence_of_element_located((By.XPATH, "/html/body/div[1]/div[1]/div/div[3]/div[3]"))
        )

        with open('auth.json', 'w') as f:
            data = json.dumps({
                auth_user: self.driver.get_cookies()
            })
            f.write(data)
