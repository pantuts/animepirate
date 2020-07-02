#!/usr/bin/env python3

from bs4 import BeautifulSoup
from animepirate import config
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
import requests


class VSParser:
    def __init__(self, url, driver):
        self.driver = driver
        self.url = url
        self.retries = 0
        self.video = ''

    def parse(self):
        if self.retries == config.MAX_RETRIES:
            print(f'[-] Unable to get video url: {self.url}')
            self.retries = 0
            return

        try:
            print(f'[+] Parsing video: {self.url}')
            sites = self._get_streaming_sites()
            if 'Mp4upload' in sites:
                self.driver.get(self.url)
                WebDriverWait(self.driver, 15).until(EC.presence_of_element_located((By.CLASS_NAME, 'anime_muti_link')))
                self.driver.find_element_by_class_name('anime_muti_link').find_element_by_partial_link_text('MP4UPLOAD').click()

                soup = BeautifulSoup(self.driver.page_source, 'lxml')
                iframe = soup.find('iframe').get('src')
                if 'gogoanime' in iframe:
                    self.driver.get(iframe)
                    soup = BeautifulSoup(self.driver.page_source, 'lxml')
                    self.video = soup.find('source').get('src')
                    print(f'[+] Parsed: {self.video}')
                    self.retries = 0
            else:
                print(f'[!] Supports Mp4upload streaming site only, find other source instead.')
        except Exception:
            self.retries += 1
            self.parse()

    def _get_streaming_sites(self):
        s = []
        try:
            resp = requests.get(self.url)
            soup = BeautifulSoup(resp.text, 'lxml')
            s = [a.find('i').next.strip() for a in soup.select('.anime_muti_link li a')]
        except Exception as e:
            print(e)
            pass
        return s
