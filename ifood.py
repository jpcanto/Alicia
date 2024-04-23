from selenium import webdriver
from selenium.webdriver.common.keys import Keys as sl_keys
from selenium.webdriver.common.by import By as sl_by
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service as sl_sv
from selenium.webdriver.chrome.options import Options as sl_opts

from imbox import Imbox
from email.message import EmailMessage

from datetime import date, datetime
import time
import re
import json
import os

from threading import Thread

from config import config
from logger import logger


class Ifood:
    def __init__(self):
        self.email = config["GMAIL_USR"]
        self.password = config["GMAIL_PASS"]
        self.phone = config["PHONE_NUMBER"]
        self.final_value = 0
        self.callback = []

        self.run()

    def run(self):
        # def open_ifood(self):
        print(self.password)
        chrome_options = sl_opts()
        # chrome_options.add_argument("--headless")

        self.driver = webdriver.Chrome(
            service=sl_sv(ChromeDriverManager().install()), options=chrome_options
        )
        self.driver.get("https://www.ifood.com.br/inicio")
        assert "iFood" in self.driver.title

        self.do_login()

    def do_login(self):
        try:
            self.driver.find_element(
                sl_by.XPATH, "//*[contains(text(), 'Entrar ou cadastrar')]"
            ).click()
            self.driver.find_element(
                sl_by.XPATH, "//*[contains(text(), 'E-mail')]"
            ).click()

            self.driver.find_element(sl_by.NAME, "email").send_keys(
                self.email + sl_keys.RETURN
            )

            try:
                self.ifood_messages_list = self.get_ifood_emails()

                while self.ifood_messages_list == None:
                    self.retry_login()

                subject = self.ifood_messages_list[-1].subject

                if "é o seu código de acesso" in subject:
                    for i, code in enumerate(subject[:6]):
                        self.driver.find_element(sl_by.ID, f"otp-input-{i}").send_keys(
                            code
                        )

                self.clear_code_if_expired()
                self.input_phone_number()
                self.access_home_address()

            except Exception as err:
                logger.error(f"An error ocurred trying to input e-mail code: {err}")
        except Exception as err:
            logger.error(f"An error ocurred trying to receive e-mail code: {err}")

    def get_ifood_emails(self):
        time.sleep(5)
        mail = Imbox("imap.gmail.com", username=self.email, password=self.password)
        ifood_messages = mail.messages(
            sent_from="naoresponder@login.ifood.com.br",
            date__gt=date.today(),
        )
        return [msg for uid, msg in ifood_messages]

    def retry_login(self):
        logger.info("Access code not received... trying again")
        self.driver.find_element(
            sl_by.XPATH,
            "//*[contains(text(), 'Não recebi meu código')]",
        ).click()
        self.driver.find_element(
            sl_by.XPATH,
            "//*[contains(text(), 'Reenviar código')]",
        ).click()

        self.ifood_messages_list = self.get_ifood_emails()

    def clear_code_if_expired(self):
        try:
            time.sleep(1.5)
            self.driver.find_element(
                sl_by.XPATH,
                '//*[contains(text(), "Código expirado ou inválido")]',
            )
            for i in range(6):
                self.driver.find_element(sl_by.ID, f"otp-input-{i}").send_keys(
                    sl_keys.BACK_SPACE
                )
        except:
            pass

    def input_phone_number(self):
        try:
            self.driver.find_element(
                sl_by.XPATH, "//*[contains(text(), 'Qual é o número do seu celular?')]"
            )
            self.driver.find_element(sl_by.NAME, "phoneNumber").send_keys(self.phone)
            self.driver.find_element(
                sl_by.XPATH, "//label[contains(text(), 'WhatApp')]"
            ).click()
        except:
            pass

    def access_home_address(self):
        while True:
            try:
                self.driver.find_element(
                    sl_by.CSS_SELECTOR, "[aria-label=Casa]"
                ).click()
                break
            except:
                time.sleep(5)


i = Ifood()
