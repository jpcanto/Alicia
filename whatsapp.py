from selenium import webdriver
from selenium.webdriver.common.keys import Keys as sl_keys
from selenium.webdriver.common.by import By as sl_by
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as sl_sv
from selenium.webdriver.chrome.options import Options as sl_opts

import time

from config import config
from logger import logger
from alicia import Alicia


class Whatsapp:
    def __init__(self):
        self.target_name = "iFood"
        self.app_data = config["LOCAL_APPDATA"]
        self.chrome_user_data = rf"{self.app_data}Google\Chrome\User Data"
        self.alicia = Alicia()

        self.run()

    def run(self):
        self.init_driver()
        self.do_login()

    def init_driver(self, login_needed=False):
        chrome_options = sl_opts()
        chrome_options.add_argument(f"user-data-dir={self.chrome_user_data}")
        
        logger.info("iniciando driver", login_needed=login_needed)

        if not login_needed:
            chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            service=sl_sv(ChromeDriverManager().install()), options=chrome_options
        )
        self.driver.get("https://web.whatsapp.com/")

    def do_login(self):
        login_needed = True
        
        logger.info("doing_login")

        while True:
            try:
                time.sleep(5)
                self.driver.find_element(sl_by.CSS_SELECTOR, "[aria-label='Scan me!']")
                self.alicia.play_audio(
                    "Preciso que você faça o login no whatsapp para resgatar o código de acesso",
                    "whatsapp_login.mp3",
                )
                if login_needed:
                    self.driver.quit()
                    self.init_driver(login_needed)
                    login_needed = False
            except:
                break

        self.init_driver(True)

    def reedem_code(self):
        while True:
            try:
                self.driver.find_element(
                    sl_by.CSS_SELECTOR, f"[title='{self.target_name}']"
                ).click()
                break
            except:
                continue

        messages_in = self.driver.find_elements(sl_by.CSS_SELECTOR, ".message-in")
        last_message_in = messages_in[-1]

        logger.info("last message", message=last_message_in)


w = Whatsapp()
