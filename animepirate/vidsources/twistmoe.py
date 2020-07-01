#!/usr/bin/env python3

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import requests


class TwistMoe:
    def __init__(self, url, driver):
        self.driver = driver
        self.url = url
        self.retries = 0
        self.video = ''

    def parse(self):
        if self.retries == 3:
            print(f'[-] Unable to get video url: {self.url}')
            self.retries = 0
            return

        try:
            print(f'[+] Parsing video: {self.url}')
            self.driver.get(self.url)
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'episode-list')))
            try:
                u1 = re.findall(r'(?=https).+\[[A-Z0-9]{8}\]\.mp4', self.driver.page_source)[0]
                resp = requests.head(u1)
                self.video = resp.headers.get('Location')
                print(f'[+] Parsed: {self.video}')
                self.retries = 0
            except Exception:
                self.retries += 1
                self.parse()
        except Exception:
            self.retries += 1
            self.parse()
