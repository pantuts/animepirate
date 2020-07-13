#!/usr/bin/env python3

from animepirate import config
from bs4 import BeautifulSoup
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import re
import requests


class VSParser:
    def __init__(self, url, driver):
        self.driver = driver
        self.url = url
        self.retries = 0
        self.video = ''
        self.ad_removed = False

    def parse(self):
        if self.retries == config.MAX_RETRIES:
            print(f'[-] Unable to get video url: {self.url}')
            self.retries = 0
            return self.video

        try:
            print(f'[+] Parsing video: {self.url}')
            self.driver.get(self.url)
            WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'stream-item')))

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            url = soup.find('iframe', {'src': re.compile(r'streaming.php')}).get('src')
            if url.startswith('//'):
                url = f'http:{url}'

            self.driver.get(url)
            self._until_ads_removed()

            soup = BeautifulSoup(self.driver.page_source, 'lxml')
            try:
                u1 = soup.find('li', {'data-video': re.compile(r'mp4upload')}).get('data-video')
            except Exception:
                print(f'[!] Supports Mp4upload streaming site only, find other source instead.')
                return

            self.driver.get(u1)
            self.video = self.driver.find_element_by_tag_name('source').get_attribute('src')
            print(f'[+] Parsed: {self.video}')
            self.retries = 0
        except Exception:
            self.retries += 1
            self.parse()

    def _until_ads_removed(self):
        while not self.ad_removed:
            try:
                self.driver.find_element_by_xpath('//body').click()
                self.driver.find_element_by_id('myVideo').click()
                self.ad_removed = True
                break
            except Exception:
                pass
