#!/usr/bin/env python3

from animepirate import config
import re
import requests


class VSParser:
    def __init__(self, url):
        self.url = url
        self.retries = 0
        self.video = ''

    def parse(self):
        if self.retries == config.MAX_RETRIES:
            print(f'[-] Unable to get video url: {self.url}')
            self.retries = 0
            return self.video

        try:
            print(f'[+] Parsing video: {self.url}')
            resp = requests.get(self.url)
            self.video = re.findall(r'((?=https).+\.mp4.+?)"', resp.text)[0]
            print(f'[+] Parsed: {self.video}')
            self.retries = 0
        except IndexError:
            return
        except Exception:
            self.retries += 1
            self.parse()
